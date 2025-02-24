import jwt
from settings import SECRET_KEY

def decode_jwt(token):
    try:
        return {"token": jwt.decode(token, SECRET_KEY, algorithms=["HS256"])}
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}