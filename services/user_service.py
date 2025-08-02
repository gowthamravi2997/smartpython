# from models.user import User
import pymysql
from pymysql.constants import CLIENT
from flask import jsonify
import hashlib
import time
import base64

config = {
    "host": "localhost",
    "user": "root",
    "password": "admin@123",
    "db": "testdb",
    # "charset": "utf8mb4",
    # "cursorclass": pymysql.cursors.DictCursor,
    "client_flag": CLIENT.MULTI_STATEMENTS
}



def verify_authorization_token(encoded_token, password, secret_key):
    try:
        # Decode from base64
        token_bytes = base64.urlsafe_b64decode(encoded_token.encode('utf-8'))
        token_string = token_bytes.decode('utf-8')
        
        # Split token parts
        username, expiry_time, token_hash = token_string.split(":")
        expiry_time = int(expiry_time)
        
        # Check expiry
        current_time = int(time.time())
        if current_time > expiry_time:
            return False, "Token expired"
        
        # Recreate hash and compare
        data = f"{username}:{password}:{expiry_time}:{secret_key}"
        expected_hash = hashlib.sha256(data.encode()).hexdigest()
        
        if expected_hash != token_hash:
            return False, "Invalid token"
        
        return True, f"Token is valid for user {username}"
    
    except Exception as e:
        return False, f"Invalid token format: {e}"

class UserService:
    users = []
    next_id = 1

    @classmethod
    def create_user(cls, user):
        connection = pymysql.connect(**config)
        try:
            with connection.cursor() as cursor:
                sql = """
                create table if not exists users (
                    id int primary key auto_increment,
                    username varchar(255),
                    email varchar(255)
                )
                """
                cursor.execute(sql)
                insert_sql = "insert into users (username, email) values (%s, %s)"
                sql = "insert into users (username, email) values (%s, %s)"
                cursor.execute(sql, (user['username'], user['email']))
                connection.commit()
                return "User created successfully",201
        except Exception as e:
            print(e)
        finally:
            connection.close()

    @classmethod
    def get_users(cls, authcode):
        is_valid, message = verify_authorization_token(authcode, "admin@123", "smart")
        print(is_valid)
        if not is_valid:
            return "Unauthorized", 401
        connection = pymysql.connect(**config)
        try:
            with connection.cursor() as cursor:
                sql = "select * from users"
                cursor.execute(sql)
                result = cursor.fetchall()
                return jsonify(result),201
        except Exception as e:
            print(e)
        finally:
            connection.close()