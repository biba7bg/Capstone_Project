import logging
import getpass


import menu_options
import services_options
from printtxtslow import print_slow
from printtxtslow import separate



# This is the start page in AbstrUtility Tool.


logging.basicConfig(level=logging.INFO, filename="abstrutility.log",
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d-%H:%M:%S')
log = logging.getLogger("abstrutility.log")


def get_credentials():
    # This Function defines the connection information, server name, username and password
    #server_name = input("Enter Server Name: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    return  username.lower(), password


# Main MENU FUNCTIONS
def main_menu():
    # This is AbsrUtility Tool main menu
    print("\nMain Menu, use only numbers: ")
    separate()
    print("1. Server Menu\n2. Network Menu\n3. Exit")
    separate()
    choice = input(" \nPlease chose an option: ")
    if choice == "1":
        # calling server menu
        server_os()
    elif choice == "2":
        # caling network menu
        network_menu()
    elif choice == "3":
        # exits the program
        print("                                    ")
        print_slow("You have decided to exit. Thanks for using AbstrUtility Tool, see you soon.")
        print("                                    ")
        separate()
        exit(0)
    else:
        log.error("Invalid choice in main  menu.")
        print("Use only numbers /1/2/3 for this menu.")
        return main_menu()
    return int(choice)

# SERVERS Operating system choice Menu
def server_os():
    # This functions makes user to define which OS he is going to work with
    print("                           ")
    print("\nServer Menu, use only numbers: ")
    separate()
    print("Choose server type:\n1. Linux Server Menu\n2. Windows Server Menu\n3. Previous Menu\n4. Quit")
    separate()
    choice = input("Enter the server type:")
    if choice == "1":
        # if choice 1 is selected, the program calls  linux server menu function
        linux_server_menu()
    elif choice == "2":
        # if choice 1 is selected, the program calls  windows server menu function
        windows_server_menu()
    elif choice == "3":
        # return to main menu
        return main_menu()
    elif choice == "4":
        print_slow("You have decided to exit. Thanks for using AbstrUtility Tool, see you soon.")
        separate()
        # quit the program
        exit(0)
    else:
        log.error("Invalid server menu")
        print("Use only numbers /1/2/3/4 for this menu.")
        return server_os()
    return int(choice)

# LINUX SERVER MENU FUNCTIONS
def linux_server_menu():
    # this is linux server menu function, which will present the user with linux options
    print("                             ")
    print("Linux Server Menu, use only numbers: ")
    separate()
    print("1. Linux Server Options Menu\n2. Linux Services Menu\n3. Previous Menu\n4. Quit")
    separate()
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
        print_slow("You have decided to exit. Thanks for using AbstrUtility Tool, see you soon.")
        separate()
        exit(0)
    else:
        log.error("Invalid choice in server menu.")
        print("Use only numbers /1/2/3/4 for this menu.")
        return linux_server_menu()
    return int(choice)

# WINDOWS SERVER MENU FUNCTIONS
def windows_server_menu():
    # this is windows server menu function, which will present the user with windows options
    print("                             ")
    print("Windows Server Menu, use only numbers: ")
    separate()
    print("1. Windows Server Options Menu\n2. Windows Services Options Menu\n3. Previous Menu\n4. Quit")
    separate()
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
        print_slow("You have decided to exit. Thanks for using AbstrUtility Tool, see you soon.")
        separate()
        exit(0)
    else:
        log.error("Invalid choice in server menu.")
        print("Use only numbers /1/2/3/4/ for this menu.")
        return windows_server_menu()
    return int(choice)


# LINUX SERVICES FUNCTIONS
def linux_service_choice():
    # This is linux services menu choice, where the user can choose from the given services choices
    print("                             ")
    print("Linux Services Menu, use only numbers: ")
    separate()
    print("1. Display all running services\n2. Last 5 reboots\n3. JVM restart\n4. List Server Resources\n5. Previous Menu\n6. Quit")
    separate()
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
        # List all resiurces
        services_options.linux_resources()
    elif choice == "5":
        # choice 4 takes user to the previous menu
        return linux_server_menu()
    elif choice == "6":
        # choice 5 exits the program
        print("                       ")
        print_slow("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        separate()
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        print("Use only numbers /1/2/3/4/5/6 for this menu.")
        return linux_service_choice()
    return int(choice)

# WINDOWS SERVICES FUNCTIONS
def windows_service_choice():
    # This is windows service menu choices function
    print("                             ")
    print("Windows Services Menu, use only numbers: ")
    separate()
    print("1. Display all services\n2. IIS Restart\n3. App Pool Restart\n4. Provide Service Name\n5. Previous Menu\n6. Quit")
    separate()
    choice = input("Enter an option: ")
    if choice == "1":
        # this choice takes the user to call all running services, the function for this is in the services_option.py file
        services_options.windows_allservices()
    elif choice == "2":
        # this choice takes the user to IIS restart, the function for this is in the services_option.py  file
        services_options.windows_IIS()
    elif choice == "3":
        # this choice takes the user to App pool restart, the function for this is in the services_option.py  file
        services_options.windows_app_pools()
    elif choice == "4":
        # this choice takes the user to restart service on demand, the function for this is in the services_option.py  file
        print("I am  option 4 in windows_service_choice")
        services_options.windows_service_input()
    elif choice == "5":
        return windows_server_menu()
    elif choice == "6":
        print("                      ")
        # choice to exit the program
        print_slow("You have decided to exit. Thanks for using AbstrUtility Tool, see you soon.")
        separate()
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        print("Invalid choice.")
        print("Use only numbers /1/2/3/4/5/6 for this menu.")
        return windows_service_choice
    return int(choice)

# NETWORK MENU FUNCTIONS
def network_menu():
    # This is network menu choices
    print("                             ")
    print("Network Menu, use only numbers: ")
    separate()
    print("1. Pathping\n2. Nslookup\n3. Subnet Scanning\n4. Previous Menu\n5. Quit")
    separate()
    choice = input("Enter an option: ")
    if choice == "1":
        # option 1 pathping is calling the function, which is defined in menu_options.py file
        pathping = menu_options.pathping_scan()
        print(pathping)
        separate()
        return network_menu()
    elif choice == "2":
        # option 2 nslookup is calling the function, which is defined in menu_options.py file
        ip_address = []
        menu_options.nslookup(ip_address)
        ip_list = input("Enter IP Addresses separated by comma: ").split(",")
        ip_list = [ip.strip() for ip in ip_list]# remove extra spaces
        lookup_results = menu_options.nslookup(ip_list)
        separate()
        for ip, hostname in lookup_results.items():
            print(f"{ip}: {hostname}")   
        print("                           ")
        print_slow("This is the end of the list")
        separate()
        return network_menu()   
    elif choice == "3":
        # option 3 subnetscan is calling the function, which is defined in menu_options.py file
        menu_options.subnet_scan()
    elif choice == "4":
        # option 4 takes user to previous menu
        main_menu()
    elif choice == "5":
        # choice 5 exits the program
        print_slow("You have decided to exit. Thanks for using AbstrUtility Tool, see you soon.")
        separate()
        # This is network menu choices
        exit(0)
    else:
        log.error("Invalid choice in service choice menu.")
        print("Use only numbers /1/2/3/4/5 for this menu.")
        return network_menu()
    return int(choice)


# Call the main menu function to start the program
if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("                                    ")
    print_slow(" Welcome  to  AbstrUtility Tool!" )
    print("                                    ")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    main_menu()
