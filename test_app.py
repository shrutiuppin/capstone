import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

# Tokens are formatted as such to limit lenght on a line
CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjgxVE1fMzF1VEczemJMbnBKTlpDNCJ9.eyJpc3MiOiJodHRwczovL2RldmVsb3Blci1mc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDNkMmZkNWViNGQ2MDAwNzBmZjMxMjEiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTYxNDY5MDYzMSwiZXhwIjoxNjE0Nzc3MDMxLCJhenAiOiI4UzVjVDFNZ0wyYTd1SkI3dnBQRGwwd3c1cDMybkh5SyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.gcUBt2uJMsd9qa9F6_8_8qoNYZGawdaAEcdJW5X0QFREJPq78TtZOfDmwkK6p2YBZp3xPoujDe7ywun5cLniEbEglm8aabggsZqZi3ZL35F6z8Mg6E8II_G-UDRGCyy4JrvjZXBWvwhHqW5BdIBAtWsKlw44Q2-twcDtOzjiIlo_pY8Q2sJpG97LCgrbFasZa8INRzDLQ7Bm2syhysPACf8KHUkZtZ14txUTJkp0zLqEXqKSDcBTKQe4W4hAgTHi9zEyFyzSv0vDZALzOOkR_OIoz3bkno1srh36z4nhBs13L4jqd0HuHDILQKud7opM3sIJ60bmwlvb1NKuvrjqWA')  

CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjgxVE1fMzF1VEczemJMbnBKTlpDNCJ9.eyJpc3MiOiJodHRwczovL2RldmVsb3Blci1mc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZmU2MDI5YTc4MjM4YjAwNzE5NmI0OGIiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTYxNDY5MDY5MSwiZXhwIjoxNjE0Nzc3MDkxLCJhenAiOiI4UzVjVDFNZ0wyYTd1SkI3dnBQRGwwd3c1cDMybkh5SyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsImdldDppbWFnZXMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0OmltYWdlcyJdfQ.IeQAS5Dmqt1hSkEv5u1E90tF3pREkQB0Q_bl0lq_FzvlrV_PGha0e4YdIK8s7OTh3bt-8NpD7rqfPw_dt6Gc8VhjoXBrJJmoNvYR4jl-Qo5kmXaaYTyAIACDeEf49IIHqF9NS9j2e7Kod_StJVefLCPqnwtFtEj2soEGJe2uevWF6qc4qpWQXdqLMkgCoY9f_QrMdEl22rA-MVJJEKfO0WeVpwJJHMwwQYVVVawh_Ta1ZkndaGZlIcCguDPE2bRUfKk1FQMYlJ5ScGwytlSsY6ZdMYUpICLiSJH2F35wFZ8_Fy6bILe_lSlIDSkReNNSA5BgH8aHIZ2OY0FBZ84-Ng')  
EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjgxVE1fMzF1VEczemJMbnBKTlpDNCJ9.eyJpc3MiOiJodHRwczovL2RldmVsb3Blci1mc3dkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MDBmZmM4YjlkYmQxYTAwNjhmMDEzMzAiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTYxNDY5MDc0NiwiZXhwIjoxNjE0Nzc3MTQ2LCJhenAiOiI4UzVjVDFNZ0wyYTd1SkI3dnBQRGwwd3c1cDMybkh5SyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTpkcmlua3MiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDpkcmlua3MtZGV0YWlsIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOmRyaW5rcyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpkcmlua3MiLCJwb3N0Om1vdmllcyJdfQ.KWaGvSLydLXdLUZGJ1DbwWfQys9lknzbpAl2WjFV2S0qWl-3mqW87rgolRSiERqm24nbs_L7g4pZPAz5SkxjR7rb8KQaN1Es4hNFDz1R3B0wsTS4id9Ou4z874ttxe1yPY_UglTIBZqvcEPk7_c0pGd1ziq5hqSgb73L8o1bGVmrnAXSIL6-p38dAs2tJ9jU7ULFZ3nUoN8cse-UcUT6s5U67kAO67w6rK_46AHpSbDfvhrt0T0MRLg2FSm66YBRcEXKcjp_IL7CkA58CvvS0Dp2h0ti6K8DixgWhdesMyAAq4cTQ_ooHEpnLRnKodyiiE6NCcO0vturyI9Bf02j0A')  


class CastingAgencyTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'name',
            'release_date': '2020-05-06',
        }
        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    #  Tests that you can get all movies
    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test to get a specific movie
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'name')

    # # tests for an invalid id to get a specific movie
    def test_404_get_movie_by_id(self):
        response = self.client().get(
            '/movies/100',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create a movie
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'name')

    # # Test to create a movie if no data is sent
    def test_400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # # tests RBAC for creating a movie
    def test_401_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # # Test to Update a movie
    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': 'title', 'release_date': "2019-11-12"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'title')

    # # Test that 400 is returned if no data is sent to update a movie
    def test_400_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # # tests RBAC for updating a movie
    def test_401_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/1',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # # tests that 404 is returned for an invalid id to get a specific movie
    def test_404_patch_movie(self):
        response = self.client().patch(
            '/movies/12323',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # # tests to delete a movie
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # # tests RBAC for deleting a movie
    def test_401_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # # tests for an invalid id to delete a specific movie
    def test_404_delete_movie(self):
        response = self.client().delete(
            '/movies/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # #  Tests that you can get all actors
    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # # Test to get a specific actor
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/5',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    # # tests for an invalid id to get a specific actor
    def test_404_get_actor_by_id(self):
        response = self.client().get(
            '/actors/100',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # # Test to create an actor
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'name', 'age': 20, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'name')
        self.assertEqual(data['actor']['gender'], 'male')

    # # Test to create an actor if no data is sent
    def test_400_post_actor(self):
        response = self.client().post(
            '/actors',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # # tests RBAC for creating an actor
    def test_401_post_actor_unauthorized(self):
        response = self.client().post(
            '/actors',
            json={'name': 'name', 'age': 22, "gender": "female"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # # Test to Update an actor
    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'name', 'age': 25, "gender": "female"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'name')
        self.assertEqual(data['actor']['gender'], 'female')

    # # Test that 400 is returned if no data is sent to update an actor
    def test_400_patch_actor(self):
        response = self.client().patch(
            '/actors/3',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # # tests RBAC for updating an actor
    def test_401_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'name', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # # tests that 404 is returned for an invalid id to get a specific actor
    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor/12323',
            json={'name': 'name', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # # tests to delete an actor
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # # tests RBAC for deleting an actor
    def test_401_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # # tests for an invalid id to get a specific actor
    def test_404_delete_actor(self):
        response = self.client().delete(
            '/actors/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
