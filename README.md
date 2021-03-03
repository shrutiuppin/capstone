# Casting Agency

Site live at : [https://capstone-casting-fsnd.herokuapp.com/](https://capstone-casting-fsnd.herokuapp.com/)

Capstone project for Udacity's Fullstack Nanodegree program.
Authorized users can interact with the API to view,add,update,delete Movies and Actors details. The motication behind this project is to gain knowledge about full stack 

### Endpoints

#### GET /movies

- General:

  - Returns all the movies.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies`

```json
{
  "movies": [
    {
      "id": 1,
      "release_date": "date",
      "title": "name"
    },
    {
      "id": 2,
       "release_date": "date",
      "title": "name"
    }
  ],
  "success": true
}
```

#### GET /movies/\<int:id\>

- General:

  - Route for getting a specific movie.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/1`

```json
{
  "movie": {
    "id": 1,
    "release_date": "date",
    "title": "title"
  },
  "success": true
}
```

#### POST /movies

- General:

  - Creates a new movie based on a payload.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{ "title": "title", "release_date": "date" }'`

```json
{
  "movie": {
    "id": 3,
    "release_date": "date",
    "title": "title"
  },
  "success": true
}
```

#### PATCH /movies/\<int:id\>

- General:

  - Patches a movie based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X POST -H "Content-Type: application/json" -d '{ "title": "title", "release_date": "date" }'`

```json
{
  "movie": {
    "id": 3,
    "release_date": "date",
    "title": "title"
  },
  "success": true
}
```

#### DELETE /movies/<int:id\>

- General:

  - Deletes a movies by id form the url parameter.
  - Roles authorized : Executive Producer.

- Sample: `curl http://127.0.0.1:5000/movies/3 -X DELETE`

```json
{
  "message": "deleted",
  "success": true
}
```

#### GET /actors

- General:

  - Returns all the actors.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors`

```json
{
  "actors": [
    {
      "age": 40,
      "gender": "male",
      "id": 1,
      "name": "name"
    },
    {
      "age": 50,
      "gender": "male",
      "id": 2,
      "name": "name"
    }
  ],
  "success": true
}
```

#### GET /actors/\<int:id\>

- General:

  - Route for getting a specific actor.
  - Roles authorized : Casting Assistant,Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/1`

```json
{
  "actor": {
    "age": 40,
    "gender": "male",
    "id": 1,
    "name": "name"
  },
  "success": true
}
```

#### POST /actors

- General:

  - Creates a new actor based on a payload.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -d '{ "name": "Mary", "age": 22, "gender": "female" }'`

```json
{
  "actor": {
    "age": 22,
    "gender": "female",
    "id": 3,
    "name": "name"
  },
  "success": true
}
```

#### PATCH /actors/\<int:id\>

- General:

  - Patches an actor based on a payload.
  - Roles authorized : Casting Director, Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X POST -H "Content-Type: application/json" -d '{ "name": "name", "age": 22, "gender": "female" }'`

```json
{
  "actor": {
    "age": 22,
    "gender": "female",
    "id": 3,
    "name": "name"
  },
  "success": true
}
```

#### DELETE /actors/\<int:id\>

- General:

  - Deletes an actor by id form the url parameter.
  - Roles authorized : Casting Director,Executive Producer.

- Sample: `curl http://127.0.0.1:5000/actors/3 -X DELETE`

```json
{
  "message": "deleted",
  "success": true
}
```

## Project dependencies

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

To setup vurtual environment run the following command

```bash
pipenv shell
```

#### Installing Dependencies

```bash
pipenv install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Database Setup

The project uses Postgresql as its database, you would need to create one locally and reflect it in setup.sh.
To update the database and seed run the following :

```bash
python manage.py db upgrade
python manage.py seed
```

- you may need to change the database url in setup.sh after which you can run

```bash
source setup.sh
```

- Start server by running

```bash
flask run
```

### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Pycodestyle](https://pypi.org/project/pycodestyle/) - pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

### Hosting
- Getting Started on Heroku
```
brew tap heroku/brew && brew install heroku
```

```
pip install gunicorn
pip install flask_script
pip install flask_migrate
pip install psycopg2-binary
```
- Create Heroku app
```
heroku create name_of_your_app
```
- Add git remote for Heroku to local repository
```
git remote add heroku heroku_git_url.
```
- Add postgresql add on for our database
```
heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
```
- Push it!
```
git push heroku master
```
- Run migrations
```
heroku run python manage.py db upgrade --app name_of_your_application
```

## Testing

Replace the jwt tokens in test_app.py with the ones generated on the website.

For testing locally, we need to reset database.
To reset database, run

```
python manage.py db downgrade
python manage.py db upgrade
```

### Error Handling

- 401 errors due to RBAC are returned as

```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

Other Errors are returned in the following json format:

```json
{
  "success": "False",
  "error": 422,
  "message": "Unprocessable entity"
}
```

The error codes currently returned are:

- 400 – bad request
- 401 – unauthorized
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error