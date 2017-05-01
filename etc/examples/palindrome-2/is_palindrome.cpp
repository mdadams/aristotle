#include <iostream>
#include <string>

bool is_palindrome(const std::string& word)
{
	// NOTE: THIS CODE IS INCORRECT!
	// For example, it can fail if the length of the word is even.
	std::string::const_iterator i = word.begin();
	std::string::const_iterator j = word.end();
	--j;
	while (i != j) {
		if (*i != *j) {
			return false;
		}
		++i;
		--j;
	}
	return true;
}

int main()
{
	std::string word;
	while (std::cin >> word) {
		std::cout <<
		  (is_palindrome(word) ? "palindrome\n" : "not palindrome\n");
	}
}
