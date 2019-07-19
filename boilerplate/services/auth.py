import datetime
import flask_jwt_extended as _jwt

def get_access_token(data,fresh):
    iden = {
        'username': data.get('username'),
        'role': 'viewer'
    }
    return _jwt.create_access_token(identity=iden, fresh=fresh, expires_delta=datetime.timedelta(minutes=30))