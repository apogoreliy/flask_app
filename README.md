# API and Bot

This project is composed with two parts: API and Bot.

## API
First part is an API which allows to create users, create user's posts and then like and dislike created posts. 
The API is written in Python using Flask framework. 
To store data is used SQLite database.

## Bot
Second part is an BOT to use and check the API. The Bot is also written with Python.

## Run API
This API by default uses `localhost` host and `5000` port. 
If you need to change this options, open `config.py` file and put parameters you want to use.

To run the API open the terminal and use next command: `python run_api.py`

Flask server will be automatically run and the API will be available to use

## Run Bot
To run the Bot open separate window in your terminal and paste next command: `python run_bot.py`

This command automatically invoke creating user, creating user's posts, post's likes and post's dislikes.

## User API
### PUT /api/user/signup
This endpoint is to create a user.
Should be passed `email` and `password` parameters. After successful sign up JWT token will be return.
This token will be used to authorize user.

### GET /api/user/login

This endpoint is to log in user.
Should be passed `email` and `password` parameters. After successful sign up JWT token will be return.
This token will be used to authorize user.

### GET /api/user/activity
This endpoint is to get last user's activity data like log in datetime and last activity with the API.
This endpoint returns dictionary with two fields `last_activity_at` and `logged_in_at`

### POST /api/post/
This endpoint is to create a new user's post.

### PUT /api/post/like
This endpoint is to add a like to some posts without like.

### PUT /api/post/dislike
This endpoint is to remove a like to some liked posts.

### GET /api/post/analytics
This endpoint is to get aggregated by days post's like. 
It returns a dictionary with `count` field which contain count of likes and `created_at` field which contain a data. 