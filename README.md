WECONNECT
====
[![Coverage Status](https://coveralls.io/repos/github/james947/WeConnect/badge.svg?branch=challenge_2)](https://coveralls.io/github/james947/WeConnect?branch=master)
[![Build Status](https://travis-ci.org/james947/WeConnect.svg?branch=challenge_2)](https://travis-ci.org/james947/WeConnect)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/982f0c5de2f04f318156fb8f9a095e3b)](https://www.codacy.com/app/james947/WeConnect?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=james947/WeConnect&amp;utm_campaign=Badge_Grade)
![Imgur](https://i.imgur.com/urrmxwS.png)

Features
===
The users can perform the following functions:

* Register
* Login
* Reset Password
* Register a business
* Update business profile
* Get businesses
* Get business by id
* Delete a business

Prerequisites
----
To run the Api endpoint use either of the following software:
* Postman/Curl - Testing the endpoints
* Text Editor - Making changes in the code base
*  Terminal - Run the api file

----
To Access the enpoint follow the directory.
- To access the endpoints clone the repo and cd into the following directory
* $ cd WeConnect/source/api ```api.py```

- To access the models
* $ cd WeConnect/source/models ```business.py``` ```reviews.py``` ```users.py```

- To acess the tests
* $ cd WeConnect/tests ```test_business.py``` ```test_reviews.py``` ```test_users.py```

Api endpoints
---
```
1. Users 
-  POST /api/v1/auth/register Creates user account
-  POST /api/v1/auth/login Log in user
-  POST /api/v1/auth/logout Logout user
-  PUT /api/v1/auth/reset-password Resets user password

2. Businesses
-  POST /api/v1/businesses Register new business
-  GET /api/v1/businesses List all available businesses
-  PUT /api/v1/businesses/<business_id> Update business 
-  DELETE /api/v1/businesses/<business_id> Remove business

3. Reviews
-  POST /api/v1/businesses/<business_id>/reviews Review a business
-  GET /api/v1/businesses/<business_id>/reviews Get business' reviews
```

Running the API
---
1. To run the API cd into ```$ cd WeConnect```
2. Create a virtual environment to install your dependencies.
* ```virtualenv -p python3 venv``` for mac and linux users
* ```virtualenv venv``` for windows users
3. Activate the virtual environment to install dependecies.
* ```source venv/bin/activate``` for mac and linux users
* ```source venv/scripts/activate``` for windows users
4. Install the requirements
```pip -r requirements.txt``` use the command to install dependecies.(mac,linux,windows)
5. Finally write the following command in your terminal ```python run.py```

Running tests
---
To run the tests assert that the virtual environment is activated:

* Activate virtual env
* Install pip requirements - ```pip -r requirements.txt```
* Run the following command in your terminal ```nosetests```

Built With
---
1. Flask 
2. Json {}

Documentation
---
[I'm an inline-style link](https://documenter.getpostman.com/view/4227673/collection/RW1YpLqd)

Versioning
---
- Version 0.0.1

Contributing
---
- Contributing to the development of this app is allowed just fork it!!!
  do changes and create a pull request...

Authors
---
* James Muriuki

Acknowledgments
---
1. Andela kenya
2. Flavian 
3. PMusonye
4. Georgreen
