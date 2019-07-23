# coding=utf-8
import json
import logging

from boilerplate import models as m
from boilerplate.tests.api import APITestCase
import flask_jwt_extended as _jwt
import bcrypt

__author__ = 'Kien'
_logger = logging.getLogger(__name__)


class ChangePasswordApiTestCase(APITestCase):
    def url(self):
        return '/api/users/change'

    def method(self):
        return 'POST'

    def test_change_password_when_success_then_return_200_code_and_edit_user_password_hash(self):
        valid_user = {
            'id': '1',
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password_hash': '$2b$12$SMCmEX7auWLjdolzXKBz0u/.T.is6SPz36xp6FkhxH4UT8VcnD2EW',
            'fullname': 'Nguyen Van A',
            'gender': 'male'
        }
        valid_data = {
            'oldpass': 'Nghia123',
            'newpass': 'Nghia12345',
        }
        headers = {
            'Authorization': 'Bearer ' + _jwt.create_access_token({'username': valid_user['username']}, True)
        }
        user = m.User(**valid_user)
        m.db.session.add(user)
        m.db.session.commit()

        rv = self.send_request(data=valid_data, headers=headers)

        us = m.User.query.get(valid_user['id'])
        self.assertEqual(True, bcrypt.checkpw(valid_data['newpass'].encode('utf-8'), us.password_hash.encode('utf-8')))
        self.assertEqual(200, rv.status_code)

    def test_change_password_when_invalid_data_then_return_400_code(self):
        valid_user = {
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password_hash': '$2b$12$SMCmEX7auWLjdolzXKBz0u/.T.is6SPz36xp6FkhxH4UT8VcnD2EW',
            'fullname': 'Nguyen Van A',
            'gender': 'male'
        }
        invalid_datas = [
            {
                'oldpass': 'Nghia12345',
                'newpass': 'Hello1234',
            },
            {
                'oldpass': '',
                'newpass': 'Hello1234',
            },
            {
                'oldpass': 'Nghia12345',
                'newpass': '',
            },
            {
                'oldpass': '',
                'newpass': '',
            },
        ]
        headers = {
            'Authorization': 'Bearer ' + _jwt.create_access_token({'username': valid_user['username']}, True)
        }
        user = m.User(**valid_user)
        m.db.session.add(user)
        m.db.session.commit()

        for invalid_data in invalid_datas:
            rv = self.send_request(data=invalid_data, headers=headers)
            self.assertEqual(400, rv.status_code)

    def test_change_password_and_check_5_last_pass_then_return_response_code(self):
        valid_user = {
            'id': '1',
            'username': 'helloworld',
            'email': 'hnnghia2@example.com',
            'password_hash': '$2b$12$SMCmEX7auWLjdolzXKBz0u/.T.is6SPz36xp6FkhxH4UT8VcnD2EW',
            'fullname': 'Nguyen Van A',
            'gender': 'male'
        }
        # password NghiaHello1 -> NghiaHello5
        history_pass = [
            {
                'user_id': 1,
                'password_hash': '$2b$12$l/5tv85TYah7pad3rnh28O4fzMILccQ4NWlu/WYdRmcQpnCKjnpDq'
            },
            {
                'user_id': 1,
                'password_hash': '$2b$12$GQQ9NDy1x/JkFGfpnNQOVue1VJnNX56XT3h2U.h7cgmrH7lF8p0Cm'
            },
            {
                'user_id': 1,
                'password_hash': '$2b$12$LxJpvVtXYTqKgooB.IGep.fmfTUYgwx2ApZKJewyVIemT5fEADxYW'
            },
            {
                'user_id': 1,
                'password_hash': '$2b$12$mmhonMpUVGlTStTnMfXAQ.MLlfd692gpV4wEUpZg.pX8Sf6Y7xfVa'
            },
            {
                'user_id': 1,
                'password_hash': '$2b$12$jvBt0kMKw1QlhHZ0Ry4y1Owe4E1tQHn51KeQrcFO/i6RNvvDK8eSy'
            },
        ]

        headers = {
            'Authorization': 'Bearer ' + _jwt.create_access_token({'username': valid_user['username']}, True)
        }
        user = m.User(**valid_user)
        m.db.session.add(user)
        m.db.session.commit()
        for his in history_pass:
            m.db.session.add(m.History_pass(**his))

        m.db.session.commit()

        def gen_data(num):
            return {
                'oldpass': 'Nghia123',
                'newpass': 'NghiaHello{}'.format(num)
            }
        for i in range(4):
            rv = self.send_request(data=gen_data(i+1), headers=headers)
            self.assertEqual(400, rv.status_code)

        rv = self.send_request(data=gen_data(100), headers=headers)
        self.assertEqual(200,rv.status_code)