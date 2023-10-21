import subprocess
import getpass
import subprocess
import paramiko
import main


def get_credentials():  # creating credentials function
    username = "bilyanabily"  # input("Enter your username:"4
    password = getpass.getpass("Enter your password: ")
    return username, password


# functions for server options

def linux_server_reboot():
    # print("I am linux reboot function")
    print("1. Linux Restart\n2. Linux Shutdown\n3. Return\n4. Quit")
    choice = input(" Enter desired action:")
    if choice == "1":
        # print("write code for  linux server reboot")
        confirm = input(
            "Are you sure you want to restart the server? (yes/no): ")
        if confirm.lower() == "yes":
            server_name = "192.168.1.126"  # input(" Enter server name")
            username, password = get_credentials()
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
                ssh_client.connect(
                    server_name, username=username, password=password)
                stdin, stdout, stderr = ssh_client.exec_command(
                    "sudo /sbin/reboot")
                reboot = str(stdout.read().decode('utf-8'))
                print(reboot)
            except paramiko.AuthenticationException:
                print(" Authentication failed, please verify your credentials.")
            except paramiko.SSHException as e:
                print(f"Unable to establish SSH connection: {str(e)}")
            except Exception as e:
                print(f"Error occured: {str(e)}")
            finally:
                ssh_client.close()
            return main.linux_server_menu
        else:
            return linux_server_reboot
    elif choice == "2":
        print("write code for  linux  server shutdown")
    elif choice == "3":
        return main.linux_server_menu()
    elif choice == "4":
        exit(0)
    else:
        main.logging.debug("Invalid server menu")
        print("Invalid choice")
    return int(choice)


def windows_server_reboot():
    print(" I am windows server reboot function")


# Functions for services options


def linux_allservices():
    print("I am linux server all services dislay function")
    server_name = "192.168.1.126"
    username, password = get_credentials()

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(
            "systemctl --type=service")
        services = str(stdout.read().decode('utf-8'))
        print(services)
    except paramiko.AuthenticationException:
        print(" Authentication failed, please verify your credentials.")
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection: {str(e)}")
    except Exception as e:
        print(f"Error occured: {str(e)}")
    finally:
        ssh_client.close()
    return main.linux_service_choice()


def linux_last5_reboots():
    print("I am linux server all services dislay function")
    server_name = "192.168.1.126"
    username, password = get_credentials()

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_name, username=username, password=password)
        stdin, stdout, stderr = ssh_client.exec_command(
            "uptime && last reboot | head -n 5")
        services = str(stdout.read().decode('utf-8'))
        print(services)
    except paramiko.AuthenticationException:
        print(" Authentication failed, please verify your credentials.")
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection: {str(e)}")
    except Exception as e:
        print(f"Error occured: {str(e)}")
    finally:
        ssh_client.close()
    return main.linux_service_choice()


def linux_JVM():
    print("I am linux JVM restart function")
