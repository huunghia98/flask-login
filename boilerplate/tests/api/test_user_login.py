# coding=utf-8
import json
import logging

from boilerplate import models as m
from boilerplate.tests.api import APITestCase

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


class LoginApiTestCase(APITestCase):
    def url(self):
        return '/api/users/login'

    def method(self):
        return 'POST'

    def test_login_user_when_success_then_return_user_response(self):
        valid_user = {
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password_hash': '$2b$12$SMCmEX7auWLjdolzXKBz0u/.T.is6SPz36xp6FkhxH4UT8VcnD2EW',
            'fullname': 'Nguyen Van A',
            'gender': 'male'
        }
        valid_data = {
            'username': 'helloworld',
            'password': 'Nghia123',
        }
        user = m.User(**valid_user)
        m.db.session.add(user)
        m.db.session.commit()

        rv = self.send_request(data=valid_data)

        self.assertEqual(200, rv.status_code)
        self.assertIn('access_token', rv.get_json())

    def test_login_user_when_invalid_data_then_return_400_code(self):
        invalid_datas = [
            {
                'username': '',
                'password': 'Terces12313'
            },
            {
                'username': 'moderator',
                'password': ''
            },
            {
                'username': 'tpajpqgqqyrzrdfftdqawykokarkbpbgpuwwovcmninrhzenvssxhkjujbmcbzvjwymhgvgxeqxpiabsosfyyvxpoyfeerddgrqvtuaovgsurilwoluojjmtevqxfwhyimbylvqziyeysxtwvlpdtooxrsqeroolpykloeldwoccmwjiyewhbvtzsneramvjqsjqufemwqgmrcdyiktvkohbfoxmjpkhkgpryxagjakcjcqdiazwzgheaaupaiuq',
                'password': 'Nghia123'
            },
            {
                'username': 'helloworld',
                'password': 'tpajpqgqqyrzrdfftdqawykokarkbpbgpuwwovcmninrhzenvssxhkjujbmcbzvjwymhgvgxeqxpiabsosfyyvxpoyfeerddgrqvtuaovgsurilwoluojjmtevqxfwhyimbylvqziyeysxtwvlpdtooxrsqeroolpykloeldwoccmwjiyewhbvtzsneramvjqsjqufemwqgmrcdyiktvkohbfoxmjpkhkgpryxagjakcjcqdiazwzgheaaupaiuq'
            },
            {
                'username': 'helloworld',
                'password': 'Nghia123'
            }
        ]
        for invalid_data in invalid_datas:
            rv = self.send_request(data=invalid_data)
            self.assertEqual(400, rv.status_code)
