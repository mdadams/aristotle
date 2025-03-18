#! /usr/bin/env python

import subprocess
import json
import os
import sys
#import copy

if __name__ == "__main__":
    from tabulate import tabulate

################################################################################

# Print to standard error.
def eprint(*args, **kwargs):
    print(*args, file = sys.stderr, **kwargs)

def add_gh_token(env, token):
    env = env.copy()
    if token:
        env.update({"GH_TOKEN": token})
    return env

def run_program(args, env = os.environ, jsonify = False):
    result = {}
    try:
        run_result = subprocess.run(
            args,
            env = env,
            #capture_output=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        result.update({"stdout": run_result.stdout})
        result.update({"stderr": run_result.stderr})
        result.update({"status": run_result.returncode})
        if run_result.returncode == 0:
            if jsonify:
                result.update({
                    "stdout_json": json.loads(run_result.stdout)
                })
        else:
            result.update({"error_message": run_result.stderr})
    except subprocess.CalledProcessError as e:
        result.update({"error_message": f"cannot run program {e}"})
        result.update({"status": -1})
        #eprint(e)
    except json.JSONDecodeError:
        result.update({"error_message": f"cannot decode JSON {e}"})
        result.update({"status": -2})
        #eprint(e)
    return result

class GithubClassroom():

    def __init__(self, token = None):
        self.token = token

    # Get rate limit status for the authenticated user
    # https://docs.github.com/en/rest/rate-limit/rate-limit?apiVersion=2022-11-28#get-rate-limit-status-for-the-authenticated-user
    def get_rate_limit(self):
        args = [
            "gh",
            "api",
            "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            "/rate_limit",
        ]
        env = add_gh_token(os.environ, self.token)
        run_result = run_program(args, env = env, jsonify = True)
        if run_result["status"] != 0:
            eprint(run_result["error_message"])
            raise Exception("cannot get rate limit")
        json_value = run_result["stdout_json"]
        return json_value

    # Get an assignment
    # https://docs.github.com/en/rest/classroom/classroom?apiVersion=2022-11-28#get-an-assignment
    def get_assignment(self, assignment_id, per_page = 100):
        args = [
            "gh",
            "api",
            "--paginate",
            "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            f"/assignments/{assignment_id}?per_page={per_page}",
        ]
        env = add_gh_token(os.environ, self.token)
        run_result = run_program(args, env = env, jsonify = True)
        if run_result["status"] != 0:
            eprint(run_result["error_message"])
            raise Exception("cannot get assignment")
        json_value = run_result["stdout_json"]
        return json_value

    # List accepted assignments for an assignment
    # https://docs.github.com/en/rest/classroom/classroom?apiVersion=2022-11-28#list-accepted-assignments-for-an-assignment
    def list_accepted_assignments(self, assignment_id, per_page = 100):
        args = [
            "gh",
            "api",
            "--paginate",
            "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            f"/assignments/{assignment_id}/accepted_assignments?per_page={per_page}",
        ]
        env = add_gh_token(os.environ, self.token)
        run_result = run_program(args, env = env, jsonify = True)
        if run_result["status"] != 0:
            eprint(run_result["error_message"])
            raise Exception("cannot get accepted assignments")
        json_value = run_result["stdout_json"]
        return json_value

    # Get assignment grades
    # https://docs.github.com/en/rest/classroom/classroom?apiVersion=2022-11-28#get-assignment-grades
    # FIXME: NOT YET IMPLEMENTED

    # List classrooms
    # https://docs.github.com/en/rest/classroom/classroom?apiVersion=2022-11-28#list-classrooms
    def list_classrooms(self, per_page = 100):
        args = [
            "gh",
            "api",
            "--paginate",
            "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            "/classrooms?per_page={per_page}",
        ]
        env = add_gh_token(os.environ, self.token)
        run_result = run_program(args, env = env, jsonify = True)
        if run_result["status"] != 0:
            eprint(run_result["error_message"])
            raise Exception("cannot list classrooms")
        json_value = run_result["stdout_json"]
        return json_value

    # Get a classroom
    # https://docs.github.com/en/rest/classroom/classroom?apiVersion=2022-11-28#get-a-classroom
    def get_classroom(self, classroom_id, per_page = 100):
        args = [
            "gh",
            "api",
            "--paginate",
            "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            f"/classrooms/{classroom_id}?per_page={per_page}",
        ]
        env = add_gh_token(os.environ, self.token)
        run_result = run_program(args, env = env, jsonify = True)
        if run_result["status"] != 0:
            eprint(run_result["error_message"])
            raise Exception("cannot get classroom")
        json_value = run_result["stdout_json"]
        return json_value

    # List assignments for a classroom
    # https://docs.github.com/en/rest/classroom/classroom?apiVersion=2022-11-28#list-assignments-for-a-classroom
    def list_assignments(self, classroom_id, per_page = 100):
        args = [
            "gh",
            "api",
            "--paginate",
            "-H", "Accept: application/vnd.github+json",
            "-H", "X-GitHub-Api-Version: 2022-11-28",
            f"/classrooms/{classroom_id}/assignments?per_page={per_page}",
        ]
        env = add_gh_token(os.environ, self.token)
        run_result = run_program(args, env = env, jsonify = True)
        if run_result["status"] != 0:
            eprint(run_result["error_message"])
            raise Exception("cannot list assignments")
        json_value = run_result["stdout_json"]
        return json_value

################################################################################

def get_assignment_id(gc, classroom_name, assignment_name):

    classroom_list = gc.list_classrooms()
    index = next((i for i, d in enumerate(classroom_list) if d["name"] == classroom_name), None)
    if index == None:
        #eprint(f"classroom {classroom_name} not found")
        return None
    classroom = classroom_list[index]
    if not classroom:
        #eprint(f"classroom {classroom_name} not found in list")
        return None
    assignment_list = gc.list_assignments(classroom["id"])
    index = next((i for i, d in enumerate(assignment_list) if d["title"] == assignment_name), None)
    if index == None:
        #eprint(f"XXX {assignment_list}")
        #eprint(f"assignment {assignment_name} not found")
        return None
    assignment = assignment_list[index]
    return assignment["id"]

################################################################################

def print_rate_limit(gc):
    rate_limit = gc.get_rate_limit()
    #print(json.dumps(rate_limit, indent=2))
    remaining = rate_limit["rate"]["remaining"]
    print(f"remaining {remaining}")

################################################################################

def demo_1():

    debug_level = 0

    github_token = os.environ["GC_TOKEN"]
    assignment_name = os.environ["GC_ASSIGNMENT_NAME"]
    classroom_name = os.environ["GC_CLASSROOM_NAME"]

    print(
      "Determining submissions for: "
      "Classroom {classroom_name} "
      "Assignment {assignment_name}"
    )

    gc = GithubClassroom(token = github_token)
    print_rate_limit(gc)
    print()

    assignment_id = get_assignment_id(gc, classroom_name, assignment_name)
    submissions = gc.list_accepted_assignments(assignment_id)
    table_headers = ("\n#", "\nUsers", "Repository\nName", "Default\nBranch")
    table_data = []
    for submission_index, submission in enumerate(submissions):
        submitted = submission["submitted"]
        students = submission["students"]
        group_size = len(students)
        student_logins = "\n".join(i["login"] for i in students)
        student_login = students[0]["login"]
        repo = submission["repository"]
        repo_name = repo["name"]
        full_repo_name = repo["full_name"]
        default_branch = repo["default_branch"]
        table_data.append((submission_index, student_logins, repo_name, default_branch))
    print(
        f"Submissions for "
        f"Classroom {classroom_name} "
        f"Assignment {assignment_name}\n"
    )
    print(tabulate(table_data, headers=table_headers) + "\n")
    if debug_level >= 1:
        print(json.dumps(submissions, indent=2))

    print_rate_limit(gc)

################################################################################

def print_classrooms(gc):

    classrooms = gc.list_classrooms()
    #print(json.dumps(classrooms, indent=2))

    classroom_table_headers = ("Name", "Organization")
    classroom_table_data = []
    for classroom_item in classrooms:

        classroom_id = classroom_item["id"]
        classroom = gc.get_classroom(classroom_id)
        #print(classroom_item)
        ##print(json.dumps(classroom, indent=2))
        classroom_name = classroom["name"]
        organization_name = classroom["organization"]["login"]
        classroom_table_data.append((classroom_name, organization_name))

        print(f"Classroom: {classroom_name}\n")
        assignments = gc.list_assignments(classroom_id)
        assignment_table_headers = ("Type", "Title")
        assignment_table_data = []
        for assignment in assignments:
            #print(assignment)
            assignment_type = assignment["type"]
            assignment_title = assignment["title"]
            assignment_table_data.append((assignment_type, assignment_title))
        print(tabulate(assignment_table_data, headers=assignment_table_headers))
        print("")

    print(f"Classrooms\n")
    print(tabulate(classroom_table_data, headers=classroom_table_headers))

def demo_2():
    #github_token_env = os.environ["GC_TOKEN_ENV"]
    #github_token  = os.environ[github_token_env]
    github_token  = os.environ["GC_TOKEN"]
    gc = GithubClassroom(token = github_token)
    print_rate_limit(gc)
    print_classrooms(gc)
    print_rate_limit(gc)

################################################################################

def demo_3():
    from github import Github
    github_token = os.environ["GC_TOKEN"]
    classroom_name = os.environ["GC_CLASSROOM_NAME"]
    assignment_name = os.environ["GC_ASSIGNMENT_NAME"]
    gc = GithubClassroom(token = github_token)
    gh = Github(github_token)

    org_name = classroom_name

    assignment_id = get_assignment_id(gc, classroom_name, assignment_name)
    submissions = gc.list_accepted_assignments(assignment_id)
    for submission_index, submission in enumerate(submissions):
        submitted = submission["submitted"]
        repo = submission["repository"]
        repo_name = repo["name"]
        full_repo_name = repo["full_name"]
        default_branch = repo["default_branch"]
        print(f"{org_name} {repo_name} {default_branch}")

        full_repo_name = f"{org_name}/{repo_name}"
        repo = gh.get_repo(full_repo_name)
        commits = repo.get_commits()
        num_commits = sum(1 for _ in commits)
        print(f"number of commits: {num_commits}")

################################################################################

def main():
    demo_1()
    #demo_2()
    #demo_3()

################################################################################

if __name__ == "__main__":
    sys.exit(main())
