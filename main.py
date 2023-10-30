import logging
import getpass
import menuoptions
import services_options


# This is the start page in AbstrUtility Tool.
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
    print("1. Server\n2. Network\n3. Exit")
    choice = input(" \nPlease chose and option: ")
    if choice == "1":
        server_os()
    elif choice == "2":
        network_menu()
    elif choice == "3":
        exit()
    else:
        log.error("Invalid choice in main  menu.")
        print(" Invalid choice.")
    return int(choice)


def server_os():
    # This functions makes user to define which OS he is going to work with
    print("Choose server type:\n1. Linux\n2. Windows\n3. Previous Menu\n4. Quit")
    choice = input(" Enter the server type:")
    if choice == "1":
        # choice of linux server
        linux_server_menu()
    elif choice == "2":
        # choice of windows server
        windows_server_menu()
    elif choice == "3":
        # return to main menu
        return main_menu()
    elif choice == "4":
        # quit the program
        exit(0)
    else:
        log.error("Invalid server menu")
        print(" Invalid os choice")
    return int(choice)

# LINUX SERVER MENU FUNCTIONS


def linux_server_menu():
    # this is server menu, called form mein menu, which will give us server option
    print("1. Linux Server Reboot\n2. Linux Services Menu\n3. Previous Menu\n4. Quit")
    choice = input(" Enter desired action: ")
    if choice == "1":
        menuoptions.linux_server_interaction()
    elif choice == "2":
        linux_service_choice()
    elif choice == "3":
        return server_os()
    elif choice == "4":
        exit(0)
    else:
        log.error("Invalid choice in server menu.")
        print("Invalid choice.")
    return int(choice)

# WINDOWS SERVER MENU FUNCTIONS


def windows_server_menu():
    # This the windows menu function, where user can shoose what windows actions he can preform
    print("1. Windows Server Menu\n2. Windows Services Menu\n3. Previous Menu\n4. Quit")
    choice = input(" Enter desired action: ")
    if choice == "1":
        menuoptions.windows_server_interaction()
    elif choice == "2":
        windows_service_choice()
    elif choice == "3":
        return server_os()
    elif choice == "4":
        exit(0)
    else:
        log.error("Invalid choice in server menu.")
        print("Invalid choice.")
    return int(choice)


# LINUX SERVICES FUNCTIONS
def linux_service_choice():
    # This is linux services menu choice, where the user can choose from the given services choices
    print("1. Display all running services\n2. Last 5 reboots\n3. JVM restart\n4. Previous Menu\n5. Quit")
    choice = input(" Please enter your service choice: ")
    if choice == "1":
        # this choice takes the user to call all running services, the function for this is in the services_option  file
        services_options.linux_allservices()
    elif choice == "2":
        # this choice takes the user to call last 5 server reboots, the function for this is in the services_option  file
        services_options.linux_last5_reboots()
    elif choice == "3":
        # this choice takes the user to restart JVM, the function for this is in the services_option  file
        services_options.linux_JVM()
    elif choice == "4":
        return linux_server_menu()
    elif choice == "5":
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        print("Invalid choice.")
    return int(choice)

# WINDOWS SERVICES FUNCTIONS


def windows_service_choice():
    # This is windows service menu choices function
    print("1. Display all running services\n2. IIS restart\n3. Input Service name\n4. Previous Menu\n5. Quit")
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
        services_options.windows_service_input()
    elif choice == "4":
        return windows_server_menu()
    elif choice == "5":
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        print("Invalid choice.")
    return int(choice)

# NETWORK MENU FUNCTIONS


def network_menu():
    print("Network Menu, please use only numbers (1/2/3/4/5) for this menu")
    print("1. Bulk IP scanning\n2. Nslookup\n3. Subnet scanning\n4. Previous Menu\n5. Quit")
    choice = input("Enter an option: ")
    if choice == "1":
        print("I am option 1 in network menu function")
        menuoptions.bulkip_scan()
    elif choice == "2":
        print("I am option 2 in network menu function")
        menuoptions.nslookup()
    elif choice == "3":
        print("I am option 3 in network menu function")
        menuoptions.subnet_scan()
    elif choice == "4":
        print("I am option 4 in network menu function")
        main_menu()
    elif choice == "5":
        print("I am option 5 in network menu function")
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        print("Invalid choice")
    return int(choice)


# Call the main menu function to start the program
if __name__ == '__main__':
    main_menu()
