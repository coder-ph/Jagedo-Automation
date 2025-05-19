from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
from models import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATABASE_URL =os.getenv("DATABASE_URL") or \
               'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key')
app.config['JSON_SORT_KEYS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Test Routes
@app.route('/api/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        data = request.get_json() or {}
        return jsonify({
            'success': True,
            'message': 'POST request successful',
            'received_data': data,
            'timestamp': datetime.now().isoformat()
        })
    elif request.method == 'GET':
        return jsonify({
            'success': True,
            'message': 'GET request successful',
            'timestamp': datetime.now().isoformat()
        })




if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False))