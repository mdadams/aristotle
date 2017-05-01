#include <iostream>
#include <string>

bool is_palindrome(const std::string& word)
{
	return word == std::string(word.rbegin(), word.rend());
}

int main()
{
	std::string word;
	while (std::cin >> word) {
		std::cout <<
		  (is_palindrome(word) ? "palindrome\n" : "not palindrome\n");
	}
}
