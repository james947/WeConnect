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
* Register a business
* Update business profile
* Search for a business
* Filter searches by location and category
* Delete a business

Prerequisites
----
This are html pages and can run in any browser that supports html eg.
* Chrome , internet explorer, Safari e.t.c
* postman for accessing API endpoints

Running the API
---
Locate the app.py
----

```
  
   cd/WeConnect3
   cd/Weconnect3/routes/api.py
   Access the endpoints to use on the API with POSTMAN


```
Api endpoints
---
```
1. Users 
- `POST /api/v1/auth/register` Creates user account
- `POST /api/v1/auth/login` Log in user
- `POST /api/v1/auth/logout` Logout user
- `PUT /api/v1/auth/reset-password` Resets user password
2. Businesses
- `POST /api/v1/businesses` Register new business
- `GET /api/v1/businesses` List all available businesses
- `PUT /api/v1/businesses/<business_id>` Update business 
- `DELETE /api/v1/businesses/<business_id>` Remove business
3. Reviews
- `POST /api/v1/businesses/<business_id>/reviews` Review a business
- `GET /api/v1/businesses/<business_id>/reviews` Get business' reviews

Running tests
---
```
activate virtual env
install pip requirements
pip -r requirements.txt
run nosetests
```
Built With
---
1. HTML /CSS
2. BOOTSRAP
3. FLASK
 
 Documentation
 ---
You can access the doc weconnect13.docs.apiary.io/#

Contributing
---
Contributing to the development of this app is allowed just fork it!!!
Do changes and create a pull request...

Authors
---
* James Muriuki


Acknowledgments
=== 
1. Andela kenya
2. Cohort 25
