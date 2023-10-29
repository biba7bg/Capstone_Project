import time
import sys
import getpass
import datetime
import os
import paramiko

import main


curr_date = datetime.datetime.now()
port = 22
login_wait = 5
server_name = "192.168.1.126"  # input("Enter server name or IP address: ")

# error logging function


def errorexit(str):
    main.log.error(str)
    print("ERROR: {}".format(str))
    print("Exiting...")
    main.logging.shutdown()
    os._exit(1)


# functions for server options


def linux_server_reboot():
    # This linux  server reboot function
    print("1. Linux Restart\n2. Linux Shutdown\n3. Previous Menu\n4. Quit")
    choice = input("Enter desired action: ")
    if choice == "1":
        username, password = main.get_credentials()
        confirm = input(
            "Are you sure you want to restart the server? (yes/no): ")
        if confirm.lower() == "yes":
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
                ssh_client.connect(server_name, username=username,
                                   password=password, look_for_keys=False, allow_agent=False)
            except paramiko.AuthenticationException:
                ssh_client
                print("Bad Password! Connectionclose to {}".format(server_name))
                errorexit(
                    "Bad password, connection Failed! ({})".format(server_name))
            except Exception as e:
                print(f"Error occured: {str(e)}")
                errorexit("Connection Failed {} ({})".format(
                    str(e), server_name))

            channel = ssh_client.invoke_shell()
            time.sleep(login_wait)
            channel.send("\n\n")  # send first command
            time.sleep(2)
            resp = channel.recv(9999)
            output = resp.decode("ascii")
            print("{}\n".format(output))
            if "{}@".format(username) not in output:
                ssh_client.close()
                main.log.error(
                    "Command prompt not found! Connection closed to {}".format(server_name))
                print("Command prompt not found! Connection closed to {}".format(
                    server_name))

            channel.send("sudo -i\n")   # second commmand in
            time.sleep(2)
            resp = channel.recv(9999)
            output = resp.decode("ascii")
            print("{}\n".format(output))
            if "{}@".format(username) not in output:
                ssh_client.close()
                main.log.error(
                    "Command prompt not found! Connection closed to {}".format(server_name))
                print("Command prompt not found! Connection closed to {}".format(
                    server_name))
                errorexit("Connection failed! ({})".format(server_name))

            main.log.info("Sending password")
            channel.send("{}\n".format(password))
            time.sleep(2)
            resp = channel.recv(9999)
            output = resp.decode("ascii")
            print("{}\n".format(output))
            if "root@".format(username) not in output:
                ssh_client.close()
                main.log.error(
                    "Command prompt not found! Connection closed to {}".format(server_name))
                print("Command prompt not found! Connection closed to {}".format(
                    server_name))
                errorexit("Connection failed! ({})".format(server_name))
            else:
                channel.send("cd /var\n".format(output))

    elif choice == "2":
        print("write code for  linux  server shutdown")
        linux_shutdown()
    elif choice == "3":
        return main.linux_server_menu()
    elif choice == "4":
        exit(0)
    else:
        main.logging.debug("Invalid server menu")
        print("Invalid choice")
    return int(choice)


def windows_server_reboot():
    # This windows  server reboot function
    print("1. Windows Restart\n2. Windows Shutdown\n3. Previus Menu\n4. Quit")
    choice = input("Enter desired action: ")
    if choice == "1":
        print("write code for windows server reboot")
    elif choice == "2":
        print("write code for windows server shutdown")
    elif choice == "3":
        return main.windows_server_menu()
    elif choice == "4.":
        exit(0)
    else:
        main.logging.error("Invalid server menu")
        print("Invalid choice")
    return int(choice)


# Reboot functions

def linux_reboot():
    print("I am linux reboot function")


def linux_shutdown():
    print("I am linux shutdown function")
    # Ask the user for connection details
    server_name = "192.168.1.126"  # input(" Enter server name")
    username, password = main.get_credentials()

    # Establish an SSH client session
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(server_name,
                       username=username, password=password)

    # Execute the shutdown command
    ssh_client.exec_command('sudo shutdown -h now')

    # Close the SSH client session
    ssh_client.close()

    print(f"Sent shutdown command to server {server_name}.")


# Network Meni functions


def bulkip_scan():
    print("I am Bulk IP scanning function and I am under construction")


def nslookup():
    print("I am Bulk IP scanning function and I am under construction")


def subnet_scan():
    print("I am Bulk IP scanning function and I am under construction")
