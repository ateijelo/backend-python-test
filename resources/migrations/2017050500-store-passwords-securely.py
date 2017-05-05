import binascii
import sqlite3
import hashlib
import os
import sys

with sqlite3.Connection(sys.argv[1]) as db:
    cur = db.execute("SELECT id, password FROM users")
    for user_id, password in cur:
        salt = binascii.hexlify(os.urandom(16))
        h = salt + binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password, salt, 100000))
        db.execute("UPDATE users SET password = ? WHERE id = ?", (h, user_id))
    db.commit()
