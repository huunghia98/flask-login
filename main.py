# coding=utf-8

import os
from boilerplate import app
from dotenv import load_dotenv

_DOT_ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(_DOT_ENV_PATH)

if __name__ == '__main__':
    app.run()
