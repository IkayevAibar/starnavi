# starnavi

#### A brief guideline to run it (on Windows):

 1.Activate virtual environment
```
    .\venv\Scripts\activate
```

 2.Install the required libs for the project
```
    pip install -r requirements.txt
```
 3.Create super user

```
    python manage.py createsuperuser
```
and try to run it :D

```
    python manage.py runserver
```

## Basic models:

### ● User(from django auth, but added 1 parameter) 
### ● Post 

## Basic Features:

### ● user signup
```
 POST request to /api/users/ or /auth/users/ with data in body [username, password]
```
### ● user login
```
 POST request to /api/token/ with data in body [username, password] and you get a refresh and access tokens
```
### ● post creation
```
 POST request to /api/posts/ with data 

   [
    text -> text field 5000 max char
    published -> boolean
    is_reply -> boolean
    author -> id of user
    parent_post -> id of post or u can don't write this parameter if new post is not part of brench
   ]
```
 
### ● post like
```
 POST request to /api/likes/ with data 
  [
    user -> id of user
    post -> id of post 
  ]
```
 
### ● post unlike
```
 DELETE method to /api/likes/<like_id>
```

### ● analytics about how many likes was made. API should return analytics aggregated by day.
```
 GET request to /api/analytics/?date_from=<date_from>&date_to=<date_to>
```

### ● user activity an endpoint which will show when user was login last time and when he
mades a last request to the service.

```
 GET request to /api/users/<user_id>/activity/
```

#### additionaly i added:

```
 GET request to /api/posts/<post_id>/likes/ gives u all likes to current post with post_id
```

## all requests except post request to create user need jwt token in header that looks like:

```
 Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU1OTEyOTkzLCJqdGkiOiJiZGQ5ZWQ4ZTE0ZTE0YTllYmExMTAzMTMwYjljNjFkZiIsInVzZXJfaWQiOjF9.ChuD-xKTrE8mahv7HrpFxVahWVwZWIFnA0phekISuug
```

# Thank you for your attention :D
