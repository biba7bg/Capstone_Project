import logging
import datetime
import getpass

import menu_options
import services_options

# This is the start page in AbstrUtility Tool.

curr_date = datetime.datetime.now()
login_wait = 5


logging.basicConfig(level=logging.INFO, filename="abstrutility.log",
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
log = logging.getLogger("abstrutility.log")


def get_credentials():
    # This Function defines the connection information, server name, username and password
    server_name = input("Enter Server Name: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    return server_name, username.lower(), password


# SERVERS MENU FUNCTIONS
def main_menu():
    # This is AbsrUtility main  menu
    print("\nMain menu:")
    print("1. Server Menu\n2. Network Menu\n3. Exit")
    choice = input(" \nPlease chose an option: ")
    if choice == "1":
        server_os()
    elif choice == "2":
        network_menu()
    elif choice == "3":
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        log.error("Invalid choice in main  menu.")
        print(" Invalid choice.")
    return int(choice)

# SERVERS Menu
def server_os():
    # This functions makes user to define which OS he is going to work with
    print("\nServer OS Menu")
    print("Choose server type:\n1. Linux Server Menu\n2. Windows Server Menu\n3. Previous Menu\n4. Quit")
    choice = input("Enter the server type:")
    if choice == "1":
        # if choice 1 is selected, the program calls  linux server menu function
        linux_server_menu()
    elif choice == "2":
        # if choice 1 is selected, the program calls  windowsserver menu function
        windows_server_menu()
    elif choice == "3":
        # return to main menu
        return main_menu()
    elif choice == "4":
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        # quit the program
        exit(0)
    else:
        log.error("Invalid server menu")
        menu_options.errorexit("Wrong choice of the menu.")
    return int(choice)

# LINUX SERVER MENU FUNCTIONS
def linux_server_menu():
    print("WLinux Server Menu")
    # this is linux server menu function, which will present the user with linux options
    print("Linux Server Menu")
    print("1. Linux Server Options Menu\n2. Linux Services Menu\n3. Previous Menu\n4. Quit")
    choice = input(" Enter desired action: ")
    if choice == "1":
        # choice 1 takes the user to the linux server interaction function, which is located in menuoptions.py file
        menu_options.linux_server_interaction()
    elif choice == "2":
        # choice 2 takes the user to the linux services choice function
        linux_service_choice()
    elif choice == "3":
        # choice 3 takes user to the previous menu
        return server_os()
    elif choice == "4":
        # choice 4 exits the program
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        log.error("Invalid choice in server menu.")
        menu_options.errorexit("Wrong choice of the menu.")
    return int(choice)

# WINDOWS SERVER MENU FUNCTIONS
def windows_server_menu():
    print("Windows Server Menu")
    # this is windows server menu function, which will present the user with windows options
    print("1. Windows Server Options Menu\n2. Windows Services Options Menu\n3. Previous Menu\n4. Quit")
    choice = input(" Enter desired action: ")
    if choice == "1":
        # choice 1 takes the user to the windows server interaction function, which is located in menuoptions.py file
        menu_options.windows_server_interaction()
    elif choice == "2":
        # choice 2 takes the user to the windows services choice function
        windows_service_choice()
    elif choice == "3":
        # choice 3 takes user to the previous menu
        return server_os()
    elif choice == "4":
        # choice 4 exits the program
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        log.error("Invalid choice in server menu.")
        menu_options.errorexit("nvalid choice in Server Menu.")
    return int(choice)


# LINUX SERVICES FUNCTIONS
def linux_service_choice():
    print("Linux Services Menu")
    # This is linux services menu choice, where the user can choose from the given services choices
    print("1. Display all running services\n2. Last 5 reboots\n3. JVM restart\n4. Previous Menu\n5. Quit")
    choice = input(" Please enter your service choice: ")
    if choice == "1":
        # this choice takes the user to call all running services, the function for this is in the services_option.py file
        services_options.linux_allservices()
    elif choice == "2":
        # this choice takes the user to call last 5 server reboots, the function for this is in the services_option.py  file
        services_options.linux_last5_reboots()
    elif choice == "3":
        # this choice takes the user to restart JVM, the function for this is in the services_option.py  file
        services_options.linux_JVM()
    elif choice == "4":
        # choice 4 takes user to the previous menu
        return linux_server_menu()
    elif choice == "5":
        # choice 5 exits the program
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        menu_options.errorexit("Invalid choice in the Linux Service Menu.")
    return int(choice)

# WINDOWS SERVICES FUNCTIONS
def windows_service_choice():
    # This is windows service menu choices function
    print("1. Display all services\n2. IIS Restart\n3. App Pool Restart\n4. Choose of Service\n5. Previous Menu\n6. Quit")
    choice = input("Enter an option: ")
    if choice == "1":
        print("I am  option 1 in windows_service_choice")
        services_options.windows_allservices()
        # print(test2.mock_display_services("test_server"))
    elif choice == "2":
        print("I am option 2 in windows_service_choice")
        services_options.windows_IIS()
    elif choice == "3":
        print("I am  option 3 in windows_service_choice")
        services_options.windows_app_pools()
    elif choice == "4":
        print("I am  option 4 in windows_service_choice")
        services_options.windows_service_input()
    elif choice == "5":
        return windows_server_menu()
    elif choice == "6":
        # choice 6 exits the program
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        print("Invalid choice.")
        menu_options.errorexit("Invalid choice in the Windows Service Menu.")
    return int(choice)

# NETWORK MENU FUNCTIONS
def network_menu():
    print("Network Menu, please use only numbers (1/2/3/4/5) for this menu")
    print("1. Bulk IP scanning\n2. Nslookup\n3. Subnet scanning\n4. Previous Menu\n5. Quit")
    choice = input("Enter an option: ")
    if choice == "1":
        print("I am option 1 in network menu function")
        menu_options.bulkip_scan()
    elif choice == "2":
        print("I am option 2 in network menu function")
        menu_options.nslookup()
    elif choice == "3":
        print("I am option 3 in network menu function")
        menu_options.subnet_scan()
    elif choice == "4":
        print("I am option 4 in network menu function")
        main_menu()
    elif choice == "5":
        # choice 5 exits the program
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        menu_options.errorexit("Invalid choice in the Network Menu.")
    return int(choice)


# Call the main menu function to start the program
if __name__ == '__main__':
    main_menu()
