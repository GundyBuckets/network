# Overview

In this program, I am trying to learn more about how different systems communicate with each other over a network

This is a simple P2P chat application. To use it, you will first need to share a 16-byte encryption key with the other peer you are trying to communicate with. When you run the program, you will need to set your listening port, the IP address of the peer you are trying to communicate with, and their listening port as well. It is recommended to set your port above 1024 to avoid restricted system ports and make it easy to remember.

I wrote this software to help me get started in understanding how P2P networks work and how they are utilized. It was also good practice to learn about encryption.

[Software Demo Video](https://youtu.be/kYtKPsOaiUQ)

# Network Communication

This program is a peer to peer network

This program uses TCP and you choose what ports are used

The messages are sent in a [USERNAME]: MESSAGE format

# Development Environment

This program was developed on Windows 11 in Visual Studio Code 1.97.0

Python 3.12.9

pip 25.0 to install the following libraries
- cryptography
- playsound

These libraries can be installed with the following command "pip install [library name]"

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Geek for Geeks](https://www.geeksforgeeks.org/)
* [LinkedIn Learning](https://www.linkedin.com/learning)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* Add usernames for logging purposes
* Allow the user to choose what file chats are logged to
* Fix notification sound