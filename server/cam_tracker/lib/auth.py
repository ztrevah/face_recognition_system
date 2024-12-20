from dotenv import load_dotenv
from os import getenv
import jwt, bcrypt
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.request import Request

from cam_tracker.models import User
from cam_tracker.config import constants as CONSTANTS

load_dotenv()
SECRET_JWT_ACCESS_KEY = getenv('SECRET_JWT_ACCESS_KEY')
SECRET_JWT_REFRESH_KEY = getenv('SECRET_JWT_REFRESH_KEY')

def hashedpassword(password: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(password, 'utf-8'), salt).decode('utf-8')

def checkpassword(password: str, hashed_password: str):
    return bcrypt.checkpw(bytes(password, 'utf-8'), bytes(hashed_password, 'utf-8'))

def create_access_token(user: User):
    return jwt.encode(
        payload={
            'id': str(user.id),
            'exp': round(datetime.timestamp(datetime.now() + timedelta(seconds=CONSTANTS.ACCESS_TOKEN_MAX_AGE)))
        },
        key=SECRET_JWT_ACCESS_KEY,
        algorithm=CONSTANTS.JWT_ALGORITHM
    )

def create_refresh_token(user: User):
    return jwt.encode(
        payload={
            'id': str(user.id),
            'exp': round(datetime.timestamp(datetime.now() + timedelta(seconds=CONSTANTS.REFRESH_TOKEN_MAX_AGE)))
        },
        key=SECRET_JWT_REFRESH_KEY,
        algorithm=CONSTANTS.JWT_ALGORITHM
    )

def verify_access_token(access_token: str):
    try:
        payload = jwt.decode(
            access_token,
            key=SECRET_JWT_ACCESS_KEY, 
            algorithms=CONSTANTS.JWT_ALGORITHM, 
            options={
                'verify_signature': True,
                'verify_exp': True
            }
        )
        user = User.objects.get(id=payload.get('id'))
        return user
    except Exception as e:
        return None

def verify_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            key=SECRET_JWT_REFRESH_KEY, 
            algorithms=CONSTANTS.JWT_ALGORITHM, 
            options={
                'verify_signature': True,
                'verify_exp': True
            }
        )
        user = User.objects.get(id=payload.get('id'))
        return user
    except Exception as e:
        return None
    
def current_user(req: Request):
    try: 
        access_token = req.COOKIES.get('access_token', None)
        refresh_token = req.COOKIES.get('refresh_token', None)
        user = verify_access_token(access_token)
        if user is None:
            user = verify_refresh_token(refresh_token)

        return user
    except Exception as e: 
        return None
    


def set_jwt_cookie(user: User, response: Response):
    response.set_cookie(
        'access_token',
        create_access_token(user),
        httponly=True, secure=True,
        samesite='none',
        max_age=CONSTANTS.ACCESS_TOKEN_MAX_AGE)
    response.set_cookie(
        'refresh_token',
        create_refresh_token(user),
        httponly=True, secure=True,
        samesite='none',
        max_age=CONSTANTS.REFRESH_TOKEN_MAX_AGE)
    return response

def delete_jwt_cookie(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

def verify(req: Request, res: Response):
    verified = False
    try: 
        user = current_user(req)
        if user is not None:
            set_jwt_cookie(user, res)
            verified = True
    except Exception as e:
        print(e)
        pass
    finally:
        return verified, res
    
