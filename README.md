# Capstone_Project

# Capstone_Project
1. Run the main.exe file 
2. Set up python environment and run with python
---
# Capstone_Project . exe file
 Open the folder called AbstrUtility and run the .exe file

---
## How to setup environment (One-time setup)
1. Install **Python 3.x** to **c:\python3**

2. After Python is installed add/update the following modules with these commands:

    >`python -m pip install --upgrade pip`
    `pip install --upgrade setuptools wheel pywin32 pylint ptpython`
    `pip install virtualenv virtualenv-clone virtualenvwrapper`

3. Create a base folder to store python code in (ex: c:\work\projects\python\ )

4. Copy the project folder to your new base folder

5. Open a command prompt and change the working directory to your project:
    >`cd c:\work\projects\python\Capsotne_Project`

6. Run the following commands to setup the environment for the project:

    >`python -m venv venv`
    `.\venv\Scripts\activate.bat`
    `python -m pip install --upgrade pip`
    `pip install --upgrade -r requirements.txt`

7. You should be ready to run the script:

    >`python main.py`

---
## How to run in the future (after the initial setup steps from above)

1. Open command prompt and CD to the script folder:
    >`cd c:\work\projects\Capstone_Project`

2. Activate the Python Virtual Environment:
    >`.\venv\Scripts\activate.bat`

3. Run the script:
    >`python main.py`

