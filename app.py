import os
from flask import Flask, request, jsonify
from models import setup_db, Movies, Actors
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route("/")
    def home():
      return "<h1>Home</h1>"

    @app.route('/movies', methods=["GET"])
    def get_movies():
      formatted_movies = [movie.format() for movie in Movies.query.all()]
      return jsonify({'movies':formatted_movies})

    @app.route('/actors', methods=["GET"])
    def get_actors():
      formatted_actors = [actor.format() for actor in Actors.query.all()]
      return jsonify({'actors':formatted_actors})

    @app.route('/movies', methods=["POST"])
    def post_movies():
      movie_title = request.json.get("title")
      movie_date = request.json.get("releaseDate")
      movie = Movies(title=movie_title, releaseDate=movie_date)
      movie.insert()
      return jsonify({'movies':movie.format()})

    @app.route('/actors', methods=["POST"])
    def post_actors():
      actor_name = request.json.get("name")
      actor_age = request.json.get("age")
      actor_gender = request.json.get("gender")
      actor = Actors(name=actor_name, age=actor_age, gender=actor_gender)
      actor.insert()
      print(actor.format())
      return 'True'

    @app.route('/movies/<int:id>', methods=["DELETE"])
    def delete_movies(id):
      movie = Movies.query.get(id)
      if not movie:
        return "junk delete"
      movie.delete()
      return 'True'

    @app.route('/actors/<int:id>', methods=["DELETE"])
    def delete_actors(id):
      actor = Actors.query.get(id)
      if not actor:
        return "junk delete"
      actor.delete()
      return 'True'

    @app.route("/movies/<int:id>", methods=["PATCH"])
    def patch_movies(id):
        movie_title = request.json.get("title")
        movie_date = request.json.get("releaseDate")
        movie = Movies.query.get(id)
        if not movie:
            return "DNE"

        if movie_title:
            movie.title = movie_title

        if movie_date:
            movie.releaseDate = movie_date
        movie.update()
        return "True"

    @app.route("/actors/<int:id>", methods=["PATCH"])
    def patch_actors(id):
        actor_name = request.json.get("name")
        actor_age = request.json.get("age")
        actor_gender = request.json.get("gender")
        actor = Actors.query.get(id)
        if not actor:
            return "DNE"

        if actor_name:
            actor.name = actor_name

        if actor_age:
            actor.age = actor_age

        if actor_gender:
            actor.gender = actor_gender
        
        actor.update()
        return "True"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()