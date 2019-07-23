# coding=utf-8
import json
import logging
import datetime
from boilerplate import models as m
from boilerplate.tests.api import APITestCase

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


class ActiveAccountApiTestCase(APITestCase):
    def url(self):
        return '/api/users/active/'

    def method(self):
        return 'GET'

    def test_active_account_when_success_then_move_from_signup_user_to_user_and_return_200_code(self):
        valid_user = {
            'id': '1',
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password': 'Nghia123',
            'fullname': 'Nguyen Van A',
            'gender': 'male',
            'active_token': 'adfklajfdlkjadghajqpuerqoerajaghagjafagafdfa'
        }

        user = m.Signup_user(**valid_user)
        m.db.session.add(user)
        m.db.session.commit()

        rv = self.send_request(params={'active_token': valid_user['active_token']})

        a = m.Signup_user.query.filter(m.Signup_user.username == valid_user['username']).first()
        user = m.User.query.filter(m.User.username == valid_user['username']).first()

        self.assertIsNone(a)
        self.assertIsNotNone(user)
        self.assertEqual(200, rv.status_code)

    def test_active_account_when_invalid_data_then_return_400_code(self):
        valid_user = {
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password': 'Nghia123',
            'fullname': 'Nguyen Van A',
            'gender': 'male',
            'active_token': 'kdfjakjfakjgdka;jg'
        }

        user = m.Signup_user(**valid_user)
        m.db.session.add(user)
        m.db.session.commit()

        invalid_data = {
            'active_token': 'dfakjfdjafl;dfadfadadfsf;fjg'
        }
        rv = self.send_request(params=invalid_data)
        self.assertEqual(400, rv.status_code)

    def test_active_account_when_token_expired_then_return_400_code(self):
        valid_user = {
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password': 'Nghia123',
            'fullname': 'Nguyen Van A',
            'gender': 'male',
            'token_expire_at': datetime.datetime.now(),
            'active_token': 'adkfjakgjahfkdjkncvadfjkagj'
        }

        user = m.Signup_user(**valid_user)
        m.db.session.add(user)
        m.db.session.commit()

        rv = self.send_request(params={'active_token': valid_user['active_token']})
        self.assertEqual(400, rv.status_code)