
import jwt
from django.conf import settings




class Account:
    def get_id(access_token):
        SECRET_KEY = getattr(settings, 'SECRET_KEY', None)
        payload = jwt.decode(jwt=access_token, key=SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    

