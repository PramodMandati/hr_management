# hr_management

# How to run the project

1) Install any python version which is greater than python 3.
2) Take a clone of the project.
3) Open a cmd and change the directory to the project directory.
4) Install all the packages which are in the requirements.txt with the following command.
    * pip install -r requirements.txt
5) Then run following command
    * python manage.py runserver
6) If you got any errors related to db, run the following 2 commands
    * python manage.py makemigrations
    * python manage.py migrate

# APIs

* The base url for accessing the APIs is http://127.0.0.1:8000/api

## Login API: <base_url>/login
* Authentication: username, password in the basic authentication.
* Input: None
* Output: Token, which is used for other accessing other APIs.

## Get Employees API: <base_url>/getEmployees
* Authentication: The token generated from the Login API is a Bearer token, use that token to access the present API.
* Input: None
* Output: All the employee details as shown in the Create Employee API input format.

## Create Employee API: <base_url>/createEmployee
* Authentication: The token generated from the Login API is a Bearer token, use that token to access the present API.
* Input: Check the below format
```
{
     "user": {
         "first_name": "testing",
         "last_name": "testing",
         "email": "Api@pramod.com",
         "username": "APITesting",
         "password": "testing24r"
     },
     "phone": "233423234",
     "role": "Role1",
     "team": "Team1",
     "salary": 2232323.0
 }
 ```
* Output: Same above input without password.
