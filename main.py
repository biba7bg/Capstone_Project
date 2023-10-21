import logging
import getpass
import menuoptions


# This is the start page in AbstrUtility Tool.

logging.debug("This is debug message")


def main_menu():
    # This is AbsrUtility main  menu
    print("\nMain menu:")
    print("1. Server\n2. Network\n3. Exit")
    choice = input(" \nPlease chose and option: ")
    if choice == "1":
        server_os()
    elif choice == "2":
        network_menu()
    elif choice == "3":
        exit()
    else:
        logging.debug("Invalid choice in main  menu.")
        print(" Invalid choice.")
    return int(choice)


def server_os():
    # print("I am server os choice function, and I am under construction")
    print("Choose server type:\n1. Linux\n2. Windows\n3. Return\n4. Quit")
    choice = input(" Enter the server type:")
    if choice == "1":
        print("New function, use library for linux ")
        linux_server_menu()
    elif choice == "2":
        print("New function, use library for windows ")
        windows_server_menu()
    elif choice == "3":
        return main_menu()
    elif choice == "4":
        exit(0)
    else:
        logging.error("Invalid server menu")
        print(" Invalid os choice")
    return int(choice)


def linux_server_menu():
    print("I am linux server menu function, and I am under construction")


def windows_server_menu():
    print("I am windows server menu function, and I am under construction")

# services menues


def linux_service_choice():
    print("I am linux services choice function, and I am under construction")


def windows_service_choice():
    print("I am windows services choice function, and I am under construction")


def network_menu():
    print("I am network menu function, and I am under construction ")


# Cll the mail manu function to start the program
if __name__ == '__main__':
    main_menu()
