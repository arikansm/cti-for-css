#include <cstdio>
#include <cstring>
#include <iostream>

const char *PASSWORD_FILE = "password";
const char *USERNAME_FILE = "username";

void badLevelA()
{
  char input[5];
  char password[5];

  std::sscanf(PASSWORD_FILE, "%s", password);

  std::cout << "Enter password: ";
  std::cin >> input;
}

void badLevelB()
{
  char input[5];
  char password[5];
  char username[5];

  std::sscanf(PASSWORD_FILE, "%s", password);
  std::sscanf(USERNAME_FILE, "%s", username);

  std::cout << "Enter password: ";
  std::cin >> input;
}

int main() {
   badLevelA();
   badLevelB();
   return 0;
}

