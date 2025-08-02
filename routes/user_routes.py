from flask import Blueprint , request
from services.user_service import UserService

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return {'error': 'Missing required fields'}, 400
    print("Hi")
    return UserService.create_user(data)

@user_bp.route('/', methods=['GET'])
def get_users():
    headers = request.headers
    authCode = headers.get("Authorization")
    return UserService.get_users(authCode)
