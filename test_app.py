import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors, db_create_db, db_drop_db, add_seed_data

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "nd0044-capstone"
        self.database_path = "postgresql://postgres:password@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.add_new_movie_data = {
            "title": "Noah Test Movie",
            "releaseDate": "2020-01-01"
        }

        self.patch_movie_data = {
            "title": "Noahs Renamed Movie"
        }

        self.add_new_actor_data = {
            "name": "Jonny Actor",
            "age": "23",
            "gender": "Male"
        }

        self.patch_actor_data = {
            "age" : 30
        }

        # Token setup
        # assistant token with perms to get:movies get:actors
        self.assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FWkVRelF3UlRrd056TTVSVUUxUWpZeE5qa3dNelJCTmtNMk5rWkdNMEZDUkRJeE1EUkJOZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1yY3J3ZG1zYi5hdXRoMC5jb20vIiwic3ViIjoiQWh4NWh6Ykx6WHNTVkNVRGlJb0E1SDZXZHBjbU5yWkZAY2xpZW50cyIsImF1ZCI6InVkYWNpdHktbmQwMDQ0LWNhcHN0b25lIiwiaWF0IjoxNTg2OTYzNjI1LCJleHAiOjE1ODcwNTAwMjUsImF6cCI6IkFoeDVoemJMelhzU1ZDVURpSW9BNUg2V2RwY21OclpGIiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.hh9aAUKKJDWSa5QvGd6sDch7XH62Y0KyRs5w8X5uM5MDzaJcjEHIlD7RiIrxtOlG-C_iIi4suAuJbjCBYdPeRTMQvy8Vm-uoNrSAIw53ycEUZFkQnB0pzDk93H_0VBhYPlKWLUTUWWFXclaYgAYI6nj2vXYRUsNodv4R4qg9Lw1w8dAfQlG4iQny0QCfIjPKc_-jOGFsDn47_iFpoti7zyYvbWADucvEnvQ7GM-tcWN4mvZYxK5DPOGe1kWihRH1S_caK0e-8LRI84av_ZoQ1CqFBVQfaMPPEnr9wtMzI1D50WHYp8GEPUQ3GhiOvTeDKqSd7GlbKZGB43J0wQprSg"
        # producer token with perms to get:movies patch:movies get:actors post:actors patch:actors delete:actors
        self.director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FWkVRelF3UlRrd056TTVSVUUxUWpZeE5qa3dNelJCTmtNMk5rWkdNMEZDUkRJeE1EUkJOZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1yY3J3ZG1zYi5hdXRoMC5jb20vIiwic3ViIjoiQWh4NWh6Ykx6WHNTVkNVRGlJb0E1SDZXZHBjbU5yWkZAY2xpZW50cyIsImF1ZCI6InVkYWNpdHktbmQwMDQ0LWNhcHN0b25lIiwiaWF0IjoxNTg2OTYzNzI3LCJleHAiOjE1ODcwNTAxMjcsImF6cCI6IkFoeDVoemJMelhzU1ZDVURpSW9BNUg2V2RwY21OclpGIiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMgZGVsZXRlOmFjdG9ycyBwb3N0OmFjdG9ycyBwYXRjaDphY3RvcnMgcGF0Y2g6bW92aWVzIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwicG9zdDphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiXX0.CmGWAIsjmDLW0XT5tJR1NqdpqtHmphBEceas0ERJee83yq8fy_CdCBGgsHaI1YMnk1Jcbx6kLtwPKt_0njU-Jw7_E2wpHrqd1p8OOyNuSeC6s__grNwTR96iJ_CkrH-ITFsYxgtyKHtHXlPKKdvOO4WcWIcA1Ul-E6KLfHPpzIrqXW-FWewoTE86F0jYS-9HzpIT_lWEhWcBkkCARdYsABwLKu9Zfg_JjWKPGvRhA4Y7EyLV8WJ1y_SpkhWjP8EbiCoADIkxBWnwNAEDtJTLQp90AXuB9PqKYcS26gDaxWzmMXkd4mwgP8CBUv7ct2OdmjtwUKiVhlJGKxxhEXwsbA"
        # producer token with perms to get:movies post:movies patch:movies delete:movies get:actors post:actors patch:actors delete:actors
        self.producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FWkVRelF3UlRrd056TTVSVUUxUWpZeE5qa3dNelJCTmtNMk5rWkdNMEZDUkRJeE1EUkJOZyJ9.eyJpc3MiOiJodHRwczovL2Rldi1yY3J3ZG1zYi5hdXRoMC5jb20vIiwic3ViIjoiQWh4NWh6Ykx6WHNTVkNVRGlJb0E1SDZXZHBjbU5yWkZAY2xpZW50cyIsImF1ZCI6InVkYWNpdHktbmQwMDQ0LWNhcHN0b25lIiwiaWF0IjoxNTg2OTYzNzg2LCJleHAiOjE1ODcwNTAxODYsImF6cCI6IkFoeDVoemJMelhzU1ZDVURpSW9BNUg2V2RwY21OclpGIiwic2NvcGUiOiJnZXQ6YWN0b3JzIGdldDptb3ZpZXMgZGVsZXRlOmFjdG9ycyBkZWxldGU6bW92aWVzIHBvc3Q6YWN0b3JzIHBvc3Q6bW92aWVzIHBhdGNoOmFjdG9ycyBwYXRjaDptb3ZpZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyJdfQ.idvDHcBgGDGPbJlWSsytgKpRbmIMyJNZLpngFlMYRvxsAHQuNV4MOl8Nsd_tUuyjFRKfRxP8CCrZ-Soj-5hvqBT96bzTgEU5WO2Wt-UkPX3FuteBmkgbG0N4PbsB4pddgxN56T-usn22IEPBo52jHOwOLBPKb7CtAKr1O8Apol2MyT83qQAu-d9GwrUxQfyt4JzUaizhlfuWG8SXudTn8Sadwjua2NIiZcQsj6uOYWvjy4nsa1SmFFywTonQP03REd-LUxELxUw84dGc4xlYThzw-vm-bTGfnulnN2Qgi0eBW4HVnUA86FTmWySOjw5skr1SqB2l6SXxXvsUZwkijA"

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            db_create_db()
            add_seed_data()


    def tearDown(self):
        """Executed after reach test"""
        db_drop_db()
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    As all endpoints except root / is based on roles, every functional test uses the producer token which grants all perms
    RBAC specific tests will use different tokens and will be denoted as test_rbac_TESTNAME function definitions
    The producer role is used by default meaning all of these functional tests double as an rbac test for that role
    """

    def test_get_movies(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.producer_token)}
        res = self.client().get("/movies", headers=self.headers)  # test getting movies
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.data)
        self.assertTrue(response['success'])
        self.assertGreater(len(response['movies']), 0)
        pass

    def test_post_movie(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.producer_token)}
        res = self.client().post("/movies", json=self.add_new_movie_data, headers=self.headers)  # test posting a movie
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.data)
        self.assertTrue(response["success"])
        pass
    
    def test_patch_movie(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.producer_token)}
        res = self.client().patch("/movies/1", json=self.patch_movie_data, headers=self.headers)  # test patching a movie
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.data)
        pass

    def test_delete_movie(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.producer_token)}
        res = self.client().delete("/movies/2", headers=self.headers)  # test delete movie
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.data)
        self.assertTrue(response["success"])
        pass

    def test_get_actors(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.producer_token)}
        res = self.client().get("/actors", headers=self.headers)  # test getting actors
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.data)
        self.assertTrue(response['success'])
        self.assertGreater(len(response['actors']), 0)
        pass

    def test_post_actor(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.producer_token)}
        res = self.client().post("/actors", json=self.add_new_actor_data, headers=self.headers)  # test posting a actor
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.data)
        self.assertTrue(response["success"])
        pass
    
    def test_patch_actor(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.producer_token)}
        res = self.client().patch("/actors/1", json=self.patch_actor_data, headers=self.headers)  # test patching an actor
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.data)
        pass

    def test_delete_actor(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.producer_token)}
        res = self.client().delete("/actors/2", headers=self.headers)  # test delete actor
        self.assertEqual(res.status_code, 200)
        response = json.loads(res.data)
        self.assertTrue(response["success"])
        pass

    '''
    RBAC TEST FOR ASSISTANT
    '''
    def test_rbac_assistant_post_actor(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.assistant_token)}
        res = self.client().post("/actors", json=self.add_new_actor_data, headers=self.headers)  # test posting a actor as assistant
        self.assertEqual(res.status_code, 403)
        response = json.loads(res.data)
        self.assertEqual(response["success"],False)
        pass
    
    def test_rbac_assistant_post_movie(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.assistant_token)}
        res = self.client().post("/movies", json=self.add_new_movie_data, headers=self.headers)  # test posting a movie as assistant
        self.assertEqual(res.status_code, 403)
        response = json.loads(res.data)
        self.assertEqual(response["success"],False)
        pass
    
    '''
    RBAC TEST FOR DIRECTOR
    '''
    def test_rbac_director_post_movie(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.director_token)}
        res = self.client().post("/movies", json=self.add_new_movie_data, headers=self.headers)  # test posting a movie as director
        self.assertEqual(res.status_code, 403)
        response = json.loads(res.data)
        self.assertEqual(response["success"],False)
        pass
    
    def test_rbac_director_delete_movie(self):
        self.headers = {'Authorization' : 'Bearer {}'.format(self.director_token)}
        res = self.client().delete("/movies/3", headers=self.headers)  # test deleting a movie as director
        self.assertEqual(res.status_code, 403)
        response = json.loads(res.data)
        self.assertEqual(response["success"],False)
        pass

    def test_404(self):
        res = self.client().get("/moviesspelledwrong")  # test invalid endpoint
        self.assertEqual(res.status_code, 404)
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()