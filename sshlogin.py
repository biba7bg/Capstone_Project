import paramiko
import getpass
import subprocess
import time
import logging


def get_credentials():  # creating ceredentials function
    username = "bilyanabily"  # input("Enter your username:"4
    password = "password"  # getpass.getpass("Enter your password: ")
    return username, password


def execute_commands(ssh):  # defining menu and choices function
    while True:
        print("\nChoose an option: ")
        print("1. Display running services")
        print("2. See last 5 reboots")
        print("3. Restart JVM service")
        print("4. Restart server")
        print("5. Shutdown server")
        print("6. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")
        if choice == "1":
            stdin, stdout, stderr = ssh.exec_command(
                "systemctl --type=service")
            print(stdout.read().decode())
        elif choice == "2":
            stdin, stdout, stderr = ssh.exec_command(
                "uptime && last reboot | head -n 5")
            print(stdout.read().decode())
        elif choice == "3":
            # stdin, stdout, stderr = ssh.exec_command("pgrep -f 'jvm_name'")
            print("not ready yet")
            # old_pid = stdout.read().decode()strip()
            # print(f"old JVM OID: {old_pid}")
        elif choice == "4":
            confirm = input(
                "Are you sure you want to restart the server? (yes/no): ")
            if confirm.lower() == 'yes':
                ssh.exec_command("sudo systemctl reboot")
                # here I would like to add funtion to catch what happens at the background
                print(" Server is rebooting...")
                exit(0)
        elif choice == "5":
            print("not ready yet")
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again")


def main():
    hostname = "192.168.1.126"  # input(" Enter the server ip or host name: ")
    username, password = get_credentials()
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)

        print(f"Connected to host{hostname} successfully!")
        execute_commands(ssh)

    except paramiko.AuthenticationException:
        print("Authentication failed, please verify your credentials.")
    except paramiko.SSHException as e:
        print(f"Error occured: {str(e)}")
    finally:
        ssh.close


if __name__ == "__main__":
    main()
