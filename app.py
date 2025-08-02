from flask import Flask
from routes.user_routes import user_bp

def create_app():
    print("gowthamravi")
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    print("App created and app registered")
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0",debug=True, port=5001)