# coding=utf-8
import json
import logging

from boilerplate import models as m
from boilerplate.tests.api import APITestCase

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


class RegisterApiTestCase(APITestCase):
    def url(self):
        return '/api/users/register'

    def method(self):
        return 'POST'

    def test_create_user_when_success_then_insert_to_db_and_return_200_code(self):
        valid_data = {
            'id': '1',
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password': 'Nghia123',
            'fullname': 'Nguyen Van A',
            'gender': 'male'
        }

        res = self.send_request(data=valid_data)

        self.assertEqual(200, res.status_code)
        saved_user = m.Signup_user.query.get(valid_data['id'])

        assert saved_user
        self.assertEqual(saved_user.username, valid_data['username'])
        self.assertEqual(saved_user.email, valid_data['email'])
        self.assertEqual(saved_user.fullname, valid_data['fullname'])
        self.assertEqual(saved_user.gender.value, valid_data['gender'])

    def test_create_user_when_invalid_data_then_return_400_code(self):
        invalid_datas = [
            # username
            {
                'username': '',
                'email': 'moderator@helloworld.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            {
                'username': 'as',
                'email': 'moderator@helloworld.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            {
                'username': 'tpajpqgqqyrzrdfftdqawykokarkbpbgpuwwovcmninrhzenvssxhkjujbmcbzvjwymhgvgxeqxpiabsosfyyvxpoyfeerddgrqvtuaovgsurilwoluojjmtevqxfwhyimbylvqziyeysxtwvlpdtooxrsqeroolpykloeldwoccmwjiyewhbvtzsneramvjqsjqufemwqgmrcdyiktvkohbfoxmjpkhkgpryxagjakcjcqdiazwzgheaaupaiuq',
                'email': 'moderator@helloworld.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            # email
            {
                'username': 'moderator',
                'email': '',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            {
                'username': 'moderator',
                'email': 'moderator',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            {
                'username': 'moderator',
                'email': 'tpajpqgqqyrzrdfftdqawykokarkbpbgpuwwovcmninrhzenvssxhkjujbmcbzvjwymhgvgxeqxpiabsosfyyvxpoyfeerddgrqvtuaovgsurilwoluojjmtevqxfwhyimbylvqziyeysxtwvlpdtooxrsqeroolpykloeldwoccmwjiyewhbvtzsneramvjqsjqufemwqgmrcdyiktvkohbfoxmjpkhkgpryxagjakcjcqdiazwzgheaaupaiuq@gmail.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            {
                'username': 'moderator',
                'email': 'moderator&hel@gmail.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            # password
            {
                'username': 'moderator',
                'email': 'moderator@helloworld.com',
                'password': '',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            {
                'username': 'moderator',
                'email': 'moderator@helloworld.com',
                'password': 'asdf',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            }, {
                'username': 'moderator',
                'email': 'moderator@helloworld.com',
                'password': 'tpajpqgqqyrzrdfftdqawykokarkbpbgpuwwovcmninrhzenvssxhkjujbmcbzvjwymhgvgxeqxpiabsosfyyvxpoyfeerddgrqvtuaovgsurilwoluojjmtevqxfwhyimbylvqziyeysxtwvlpdtooxrsqeroolpykloeldwoccmwjiyewhbvtzsneramvjqsjqufemwqgmrcdyiktvkohbfoxmjpkhkgpryxagjakcjcqdiazwzgheaaupaiuq',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            # fullname
            {
                'username': 'moderator',
                'email': 'moderator@helloworld.com',
                'password': 'Nghia123',
                'fullname': '',
                'gender': 'female',
            },
            {
                'username': 'moderator',
                'email': 'moderator@helloworld.com',
                'password': 'Nghia123',
                'fullname': 'tpajpqgqqyrzrdfftdqawykokarkbpbgpuwwovcmninrhzenvssxhkjujbmcbzvjwymhgvgxeqxpiabsosfyyvxpoyfeerddgrqvtuaovgsurilwoluojjmtevqxfwhyimbylvqziyeysxtwvlpdtooxrsqeroolpykloeldwoccmwjiyewhbvtzsneramvjqsjqufemwqgmrcdyiktvkohbfoxmjpkhkgpryxagjakcjcqdiazwzgheaaupaiuq',
                'gender': 'female',
            },
            {
                'username': 'moderator',
                'email': 'moderator@helloworld.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van @$$',
                'gender': 'female',
            },
            {
                'username': 'moderator',
                'email': 'moderator@helloworld.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'hello',
            }
        ]
        for invalid_data in invalid_datas:
            rv = self.send_request(data=invalid_data)
            self.assertEqual(400, rv.status_code)

    def test_create_user_existed_in_user_then_return_400_code(self):
        valid_user = {
            'username': 'helloworld',
            'email': 'sqweqa@gmail.com',
            'password_hash': '$2b$12$SMCmEX7auWLjdolzXKBz0u/.T.is6SPz36xp6FkhxH4UT8VcnD2EW',
            'fullname': 'Nguyen Van A',
            'gender': 'male'
        }
        invalid_datas = [
            {
                'username': 'helloworld',
                'email': 'moderator@helloworld.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van A',
                'gender': 'female',
            },
            {
                'username': 'hellworldqwe',
                'email': 'sqweqa@gmail.com',
                'password': 'Nghia123',
                'fullname': 'Nguyen Van Ca',
                'gender': 'female',
            },
        ]

        user = m.User(**valid_user)
        m.db.session.add(user)
        m.db.session.commit()

        for invalid_data in invalid_datas:
            rv = self.send_request(data=invalid_data)
            self.assertEqual(400, rv.status_code)


