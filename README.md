# Pwned Pass Python tool

A brief Python GUI script that demonstrates Troy Hunt's [Pwned Password](https://haveibeenpwned.com/Passwords) service. This script allows a user to manipulate a password and view the resulting SHA1 hash and API call in real time. The user can call the API manually, via copy/paste or the browser button, or can test the password within the tool.

## Getting Started

This tool is a Python 3 based script.

### Prerequisites

This will require Python 3 installed. In Windows this may need to be [downloaded and installed](https://www.python.org/downloads/); in most Linux/Unix flavours this is installed as standard. I believe Mac follows Linux/Unix, but am unable to test.

This is written and tested in Python 3.6 under Windows. It uses Tkinter for a GUI and URLLIB, these are all standard library, so it should 'just work'.

Call it by clicking its icon, or invoking its name on command line while in the relevant folder, e.g.
```
C:\Users\You\Downloads\PwnedPassTool.py
./PwnedPassTool.py
```

## License

For clarity, this is licensed under the MIT License making it free to copy and adapt - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Troy Hunt](https://www.troyhunt.com/) and [HIBP](https://haveibeenpwned.com/)