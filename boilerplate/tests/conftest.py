# # coding=utf-8
import logging
import config
import os

import pytest

__author__ = 'Kien'
_logger = logging.getLogger(__name__)

TEST_DIR = os.path.join(config.ROOT_DIR, 'boilerplate/tests')


@pytest.fixture(scope='function', autouse=True)
def app(request):
    from boilerplate import app
    from boilerplate.models import db

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(
    'root', 'nghia123', 'localhost', 3306, 'test_login'
)
    app.test_client()
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    # test db initializations go below here
    db.create_all()

    def teardown():
        db.session.remove()
        db.drop_all()
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture
def app_class(request, app):
    if request.cls is not None:
        request.cls.app = app
