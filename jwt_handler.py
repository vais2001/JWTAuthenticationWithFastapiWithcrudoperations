
import time
import jwt
from decouple import config


JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")



def signJWT(user_id: str):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000
    }
    payload1 = {
        "user_id": user_id,
        "expires": time.time() + 600000
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_token=jwt.encode(payload1, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return{
        "access_token": token,
        "refresh_tkoen":refresh_token,
    }
    

def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
    
    
    
    
    
    
    
    
    
    
    