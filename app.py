import os
from flask import Flask, request
from models import setup_db, Movies, Actors
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greetingW

    @app.route('/movies', methods=["GET"])
    def get_movies():
      movies = Movies.query.all()
      print(movies)
      return 'True'

    @app.route('/movies', methods=["POST"])
    def post_movies():
      movie_title = request.json.get("title")
      movie_date = request.json.get("releaseDate")
      movie = Movies(title=movie_title, releaseDate=movie_date)
      movie.insert()
      print(movie.format())
      return 'True'

    @app.route('/actors', methods=["GET"])
    def get_actors():
      actors = Actors.query.all()
      print(actors)
      return 'True'




    return app

app = create_app()

if __name__ == '__main__':
    app.run()