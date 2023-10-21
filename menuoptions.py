import subprocess
import getpass
import subprocess
import manues


def get_credentials():  # creating credentials function
    username = "bilyana"  # input("Enter your username:"4
    password = "pa55word"  # getpass.getpass("Enter your password: ")
    return username, password


# functions for server options

def linux_server_reboot():
    print("I am linux reboot function")


def windows_server_reboot():
    print("I am windows reboot function")

# Functions for services options


def linux_allservices():
    print("I am linux server all services dislay function")


def linux_JVM():
    print("I am linux JVM restart function")
