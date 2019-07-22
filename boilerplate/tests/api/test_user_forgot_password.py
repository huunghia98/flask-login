# coding=utf-8
import json
import logging

from boilerplate import models as m
from boilerplate.tests.api import APITestCase

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


class ForgotPasswordApiTestCase(APITestCase):
    def url(self):
        return '/api/users/forgot'

    def method(self):
        return 'POST'

    def test_forgot_password_when_success_then_edit_recover_password_in_db_and_return_200_code(self):
        valid_user = {
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password_hash': '$2b$12$SMCmEX7auWLjdolzXKBz0u/.T.is6SPz36xp6FkhxH4UT8VcnD2EW',
            'recover_hash': '$2b$12$anpUFyEEWoXrn7p2YAxrq.lRg1x01V4YQ8bUoHnBXgMJBXnoxZA/u',
            'fullname': 'Nguyen Van A',
            'gender': 'male',
        }
        valid_data = {
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
        }
        user = m.User(**valid_user)
        m.db.session.add(user)

        rv = self.send_request(data=valid_data)
        user = m.User.query.filter(m.User.username == valid_user['username']).first()

        self.assertEqual(200, rv.status_code)
        self.assertNotEqual(valid_user['recover_hash'],user.recover_hash)

    def test_forgot_password_when_not_correct_then_return_400_code(self):
        invalid_data = {
            'username': 'helloworld',
            'email': 'hnnghia2@example',
        }
        rv = self.send_request(data=invalid_data)

        self.assertEqual(400, rv.status_code)