# Full Stack Capstone Project API

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, make sure there is a database named `nd0044-capstone`. The application inserts seed data on boot. 
Note this application uses a username of `postgres` with password of `password` From the backend folder in terminal run:


## Running the server

From within the root of the repo, first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export DATABASE_URL=postgresql://postgres:password@localhost:5432/nd0044-capstone
export FLASK_ENV=development
python app.py
```

or run `.setup.sh` depending on your system.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `DATABASE_URL` variable to `postgresql://postgres:password@localhost:5432/nd0044-capstone` tells the application where the local database is located.

## Tasks
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Endpoints

GET '/'  
GET '/actors'  
GET '/movies'  
POST '/actors'  
POST '/movies'  
PATCH '/actors/<int:id>'  
PATCH '/movies/<int:id>'  
DELETE '/actors/<int:id>'  
DELETE '/movies/<int:id>'  

##### GET '/'
- Fetches a dictionary of movies and actors
- Request Arguments: None
- Authentication: Public
- Returns: An object with keys actors and movies and a success object boolean result. actors and movies keys contain an array of their model objects
```
{
    "actors": [
        {
            "age": 23,
            "gender": "Male",
            "id": 1,
            "name": "Actor 1"
        }
    ],
    "movies": [
        {
            "id": 1,
            "releaseDate": "Wed, 01 Jan 2020 00:00:00 GMT",
            "title": "Movie 1"
        }
    ],
    "success": true
}
```

##### GET '/actors'
- Fetches a dictionary of all actors
- Request Arguments: None
- Authentication: Bearer Token must have permissions `get:actors`
- Returns: An object with actors key, that contains an array of actors key:value pairs, and a success object boolean result.
```
{
    "actors": [
        {
            "age": 23,
            "gender": "Male",
            "id": 1,
            "name": "Actor 1"
        }
    ],
    "success": true
}
```

##### GET '/movies'
- Fetches a dictionary of all movies
- Request Arguments: None
- Authentication: Bearer Token must have permissions `get:movies`
- Returns: An object with movies key, that contains an array of movies key:value pairs, and a success object boolean result.
```
{
    "movies": [
        {
            "title": "Test Title",
            "releaseDate": "Sat, 01 Feb 2020 00:00:00 GMT",
            "id": 1
        }
    ],
    "success": true
}
```

##### POST '/actors'
- Adds new actor
- Request Arguments: json object with keys `name` and `gender` and `age`
- Authentication: Bearer Token must have permissions `post:actors`
- Returns: An object with actor key, that contains the new actor key:value pairs, and a success object boolean result.
```
{
    "actor": {
        "age": 29,
        "gender": "Male",
        "id": 6,
        "name": "John Smith"
    },
    "success": true
}
```

##### POST '/movies'
- Adds new movie
- Request Arguments: json object with keys `title` and `releaseDate`
- Authentication: Bearer Token must have permissions `post:movies`
- Returns: An object with movie key, that contains the new movie key:value pairs, and a success object boolean result.
```
{
    "movie":{
        "title": "Test Title",
        "releaseDate": "Sat, 01 Feb 2020 00:00:00 GMT",
        "id": 1
    },
    "success": true
}
```

##### PATCH '/actors/<int:id>'
- Updates existing actor
- Request Arguments: endpoint passing the id to be updated and body json object with keys `name` and `gender` and `age` for only the values being updated, at least 1 is required.
- Authentication: Bearer Token must have permissions `patch:actors`
- Returns: An object with actor key, that contains the actor key:value pairs, and a success object boolean result.
```
{
    "actor": {
        "age": 29,
        "gender": "Male",
        "id": 6,
        "name": "John D Smith"
    },
    "success": true
}
```

##### PATCH '/movies/<int:id>'
- Updates existing movie
- Request Arguments: endpoint passing the id to be updated and json object with keys `title` and `releaseDate` for only the values being updated, at least 1 is required.
- Authentication: Bearer Token must have permissions `patch:movies`
- Returns: An object with movie key, that contains the movie key:value pairs, and a success object boolean result.
```
{
    "movie":{
        "title": "Test Title Updated",
        "releaseDate": "Sat, 01 Feb 2020 00:00:00 GMT",
        "id": 1
    },
    "success": true
}
```

##### DELETE '/actors<int:id>'
- Delete existing actor
- Request Arguments: endpoint passing the id to be deleted.
- Authentication: Bearer Token must have permissions `delete:actors`
- Returns: An object with deleted_actor_id key, that contains the actor id removed, and a success object boolean result.
```
{
    "deleted_actor_id": 3,
    "success": true
}
```

##### DELETE '/movies<int:id>'
- Delete existing movie
- Request Arguments: endpoint passing the id to be deleted.
- Authentication: Bearer Token must have permissions `delete:movies`
- Returns: An object with deleted_movie_id key, that contains the movie id removed, and a success object boolean result.
```
{
    "deleted_movie": 3,
    "success": true
}
```

## Testing
To run the tests, run
```
python test_app.py
```