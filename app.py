import os
from flask import Flask, request, jsonify
from models import setup_db, Movies, Actors, db_drop_db, db_create_db, add_seed_data
from flask_cors import CORS
from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    db_drop_db()
    db_create_db()
    add_seed_data()

    @app.route("/")
    def home():
      formatted_movies = [movie.format() for movie in Movies.query.all()]
      formatted_actors = [actor.format() for actor in Actors.query.all()]
      return jsonify({'success':True,'actors':formatted_actors,'movies':formatted_movies}), 200

    @app.route('/movies', methods=["GET"])
    @requires_auth("get:movies")
    def get_movies(stuff):
      formatted_movies = [movie.format() for movie in Movies.query.all()]
      return jsonify({'success':True,'movies':formatted_movies}), 200

    @app.route('/actors', methods=["GET"])
    @requires_auth("get:actors")
    def get_actors(stuff):
      formatted_actors = [actor.format() for actor in Actors.query.all()]
      return jsonify({'success':True,'actors':formatted_actors}), 200

    @app.route('/movies', methods=["POST"])
    @requires_auth("post:movies")
    def post_movies(stuff):
      movie_title = request.json.get("title")
      movie_date = request.json.get("releaseDate")
      movie = Movies(title=movie_title, releaseDate=movie_date)
      movie.insert()
      return jsonify({'success':True,'movies':movie.format()}), 200

    @app.route('/actors', methods=["POST"])
    @requires_auth("post:actors")
    def post_actors(stuff):
      actor_name = request.json.get("name")
      actor_age = request.json.get("age")
      actor_gender = request.json.get("gender")
      actor = Actors(name=actor_name, age=actor_age, gender=actor_gender)
      actor.insert()
      return jsonify({'success':True,'actor':actor.format()}), 200

    @app.route('/movies/<int:id>', methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movies(stuff, id):
      movie = Movies.query.get(id)
      if not movie:
        return jsonify({'success':False,'message':"Movie does not exist!"})
      movie.delete()
      return jsonify({'success':True,'deleted_movie_id':id}), 200

    @app.route('/actors/<int:id>', methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actors(stuff, id):
      actor = Actors.query.get(id)
      if not actor:
        return jsonify({'success':False,'message':"Actor does not exist!"})
      actor.delete()
      return jsonify({'success':True,'deleted_actor_id':id}), 200

    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def patch_movies(stuff, id):
        movie_title = request.json.get("title")
        movie_date = request.json.get("releaseDate")
        movie = Movies.query.get(id)
        if not movie:
            return jsonify({'success':False,'message':"Movie does not exist!"}), 200

        if movie_title:
            movie.title = movie_title

        if movie_date:
            movie.releaseDate = movie_date
        movie.update()
        return jsonify({'success':True,'movies':movie.format()})

    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def patch_actors(stuff, id):
        actor_name = request.json.get("name")
        actor_age = request.json.get("age")
        actor_gender = request.json.get("gender")
        actor = Actors.query.get(id)
        if not actor:
            return jsonify({'success':False,'message':"Actor does not exist!"}), 200

        if actor_name:
            actor.name = actor_name

        if actor_age:
            actor.age = actor_age

        if actor_gender:
            actor.gender = actor_gender
        
        actor.update()
        return jsonify({'success':True,'actor':actor.format()}), 200

    @app.errorhandler(AuthError)
    def auth_error(error):
      return jsonify({
        'success':False,
        'error':error.status_code,
        'message':error.error['description']
      }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()