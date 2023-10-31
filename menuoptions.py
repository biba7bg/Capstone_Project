import time
import sys
import getpass
import datetime
import os
import paramiko

import main
import services_options


curr_date = datetime.datetime.now()
port = 22
login_wait = 5

# error logging function


def errorexit(str):
    main.log.error(str)
    print("ERROR: {}".format(str))
    print("Exiting...")
    main.logging.shutdown()
    os._exit(1)


# WINDOWS SERVER RESTART FUNCTION
def windows_server_reboot(session):
    # functions which intioates windows server restart
    reboot_command = "shutdown /r /t 0"
    result = session.run_cmd(reboot_command)
    return result.status_code, result.std_out.decode().strip(), result.std_err.decode().strip()

# WINDOWS SERVER SHUTDOWN FUNCTION


def windows_server_shutdown(session):
    # functions which intioates windows server shutdown
    shutdown_command = "shutdown /s /t 0"
    result = session.run_cmd(shutdown_command)
    return result.status_code, result.std_out.decode().strip(), result.std_err.decode().strip()

# LINUX SERVER MENU FUNCTIONS


def linux_server_interaction():
    # This linux  server reboot function
    print("1. Linux Restart\n2. Linux Shutdown\n3. Previous Menu\n4. Quit")
    choice = input("Enter desired action: ")
    if choice == "1":
        server_name, username, password = main.get_credentials()
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
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        main.logging.debug("Invalid server menu")
        print("Invalid choice")
    return int(choice)


def linux_shutdown():
    print("I am linux shutdown function")
    # sudo_password = getpass.getpass("Enter your sudo password: ")
    confirm = input(
        "Are you sure you want to restart the server? (yes/no): ")
    if confirm.lower() == 'yes':
        server_name, username, password = main.get_credentials()
        # Establish an SSH client session
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(
            "sudo -i /sbin/shutdown -now", get_pty=True)
        stdin.write(password + "\n")
        stdin.flush()
        print(stdout.read().decode())
        # here I would like to add funtion to catch what happens at the background
        print(" Server is rebooting...")

        # Close the SSH client session
        ssh_client.close()
        print(f"Sent shutdown command to server {server_name}.")
        # Execute the shutdown command
        # ssh_client.exec_command('sudo shutdown -h now')
        return main.linux_server_menu()


# WINDOWS SERVER MENU FUNCTIONS
def windows_server_interaction():
    # This windows  server menu function, which displays the server options given to the user
    print("1. Windows Restart\n2. Windows Shutdown\n3. Previus Menu\n4. Quit")
    choice = input("Enter desired action: ")
    if choice == "1":
        # Make confurmation thaat user would like to proceed with the choice
        confirm = input(
            "Are you sure you want to restart the server? (yes/no): ")
        if confirm.lower() == "yes":
            # Thsi is where user s asked to put the server name/IP for the server which needs a restart
            # server_name = input(
            # "Enter the remote server IP or hostname: ").strip()
            server_name, username, password = main.get_credentials()
            # session is calling create sesssion function which is defined in service_option file
            session = services_options.create_session(
                server_name, username, password)
            status_code, stdout, stderr = windows_server_reboot(session)
            # this print is showning execution status if status is 0, that mean the command has been executed successfuly
            print(f"Command executed with status code: {status_code}")
            main.log.error(f"Output: {stdout}")
        if stderr:
            print(f"Error: {stderr}")
            print("write code for windows server reboot")
            return windows_server_reboot()
    elif choice == "2":
        confirm = input(
            "Are you sure you want to restart the server? (yes/no): ")
        if confirm.lower() == "yes":
            # Thsi is where user s asked to put the server name/IP for the server which needs a restart
            # server_name = input(
            # "Enter the remote server IP or hostname: ").strip()
            server_name, username, password = main.get_credentials()
            session = services_options.create_session(
                server_name, username, password)
            status_code, stdout, stderr = windows_server_shutdown(session)
            print(f"Command executed with status code: {status_code}")
            print(f"Output: {stdout}")
        if stderr:
            print(f"Error: {stderr}")
            print("write code for windows server reboot")
            return windows_server_reboot()
    elif choice == "3":
        return main.windows_server_menu()
    elif choice == "4.":
        print("You have decided to exit. Thanks for using AbstrUtility, see you soon.")
        exit(0)
    else:
        main.logging.error("Invalid server menu")
        print("Invalid choice")
    return int(choice)


# Network Meni functions
def bulkip_scan():
    print("I am Bulk IP scanning function and I am under construction")


def nslookup():
    print("I am Bulk IP scanning function and I am under construction")


def subnet_scan():
    print("I am Bulk IP scanning function and I am under construction")
