from flask import Flask, request, jsonify, g
import pymongo
import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from cerberus import Validator  # For request validation
import jwt  # For token-based authentication
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '#2024_flask_secret_key'

# Establish a connection to MongoDB
client = MongoClient("mongodb+srv://pradeep:DPrGbZ0hDDPnH8SJ@cluster0.jb1rloa.mongodb.net/?retryWrites=true&w=majority",server_api=ServerApi('1'))
db = client["notes_app"]

# Define collections
users_collection = db["users"]
notes_collection = db["notes"]
user_notes_collection = db["user_notes_map"]
note_history_collection = db["notes_history"]
# Cerberus schema for request validation
signup_schema = {
    'username': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
    'email': {'type': 'string', 'required': True, 'regex': "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"}
}

login_schema = {
    'email': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}

create_note_schema = {
    'title': {'type': 'string', 'required': True},
    'content': {'type': 'string', 'required': True}
}

share_note_schema = {
    'note_id': {'type': 'string', 'required': True},
    'user_ids': {'type': 'list', 'required': True}
}
# Validator instances
signup_validator = Validator(signup_schema)
login_validator = Validator(login_schema)
create_note_validator = Validator(create_note_schema)
share_note_validator = Validator(share_note_schema)

# Decorator for checking if user is logged in
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            token = token.replace('Bearer ', '')
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            g.current_user = users_collection.find_one({"_id": ObjectId(data['user_id'])})
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)

    return decorated

# Endpoint for user signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json

    # Validate request data
    if not signup_validator.validate(data):
        return jsonify({"message": "Invalid request data", "errors": signup_validator.errors}), 400

    username = data['username']
    password = data['password']
    email = data['email']

    # Check if username or email already exists
    if users_collection.find_one({"$or": [{"username": username}, {"email": email}]}):
        return jsonify({"message": "Username or email already exists"}), 400

    # Hash the password before storing
    hashed_password = generate_password_hash(password)

    # Insert the user into the database
    user_id = users_collection.insert_one({"username": username, "password": hashed_password, "email": email}).inserted_id

    return jsonify({"message": "User created successfully", "user_id": str(user_id)}), 201

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    # Validate request data
    if not login_validator.validate(data):
        return jsonify({"message": "Invalid request data", "errors": login_validator.errors}), 400

    email = data['email']
    password = data['password']

    # Find the user by email
    user = users_collection.find_one({"email": email})

    # Check if user exists and if the password is correct
    if user and check_password_hash(user["password"], password):
        token = jwt.encode({'user_id': str(user["_id"])}, app.config['SECRET_KEY'])
        return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# Endpoint for creating a new note
@app.route('/notes/create', methods=['POST'])
@token_required
def create_note():
    data = request.json

    # Validate request data
    if not create_note_validator.validate(data):
        return jsonify({"message": "Invalid request data", "errors": create_note_validator.errors}), 400

    note_doc={"title": data['title'], "content": data['content']}
    # Insert the note into the database
    note_id = notes_collection.insert_one(note_doc).inserted_id

    note_map_doc = {"user_id": g.current_user["_id"], "note_id": note_id}
    # Link the note to the current user
    user_notes_collection.insert_one(note_map_doc)

    history_doc={"version":1, "note":note_doc, "note_id":note_id,
                  "modified_at":datetime.datetime.now(),
                  "modified_by": g.current_user["_id"]
                  }
    note_history_collection.insert_one(history_doc)
    return jsonify({"message": "Note created successfully", "note_id": str(note_id)}), 201

# Endpoint for sharing a note
@app.route('/notes/share', methods=['POST'])
@token_required
def share_note():
    data = request.json

    # Validate request data
    if not share_note_validator.validate(data):
        return jsonify({"message": "Invalid request data", "errors": share_note_validator.errors}), 400

    note_id= data["note_id"]
    user_ids = data["user_ids"]
    for user_id in user_ids:
        note_map_doc = {"user_id": user_id, "note_id": note_id}
        # Link the note to the current user
        user_notes_collection.insert_one(note_map_doc)

    return jsonify({"message": "Note shared successfully", "note_id": str(note_id), "user_ids":str(user_ids)}), 201

# Endpoint for retrieving a specific note by its ID
@app.route('/notes/<id>', methods=['GET'])
@token_required
def get_note(id):
    # Find the note associated with the logged-in user's user ID
    user_note = user_notes_collection.find_one({"note_id": ObjectId(id), "user_id": g.current_user["_id"]})
    
    if user_note:
        # If the note is associated with the user, fetch the note details from notes_collection
        note = notes_collection.find_one({"_id": user_note["note_id"]})
        if note:
            return jsonify({"title": note["title"], "content": note["content"]}), 200
        else:
            return jsonify({"message": "Note not found"}), 404
    else:
        return jsonify({"message": "Note not found or unauthorized"}), 404

# Endpoint for updating an existing note
@app.route('/notes/<id>', methods=['PUT'])
@token_required
def update_note(id):
    data = request.json

    # Validate request data
    if not create_note_validator.validate(data):
        return jsonify({"message": "Invalid request data", "errors": create_note_validator.errors}), 400

    # Find the note associated with the logged-in user's user ID
    user_note = user_notes_collection.find_one({"note_id": ObjectId(id), "user_id": g.current_user["_id"]})

    if user_note:
        notes_historic = note_history_collection.find_one({"note_id": ObjectId(id)}, sort=[('version', -1)])
        new_version = notes_historic['version'] + 1

        history_doc={"version":new_version, "note":data, "note_id": ObjectId(id),
                    "modified_at":datetime.datetime.now(),
                    "modified_by": g.current_user["_id"]
                    }
        note_history_collection.insert_one(history_doc)
    
        # Update the note in the notes_collection
        updated = notes_collection.update_one({"_id": user_note["note_id"]}, {"$set": data})
        if updated.modified_count > 0:
            return jsonify({"message": "Note updated successfully"}), 200
        else:
            return jsonify({"message": "Failed to update note"}), 500
    else:
        return jsonify({"message": "Note not found or unauthorized"}), 404

# Endpoint for retrieving all changes associated with a note
@app.route('/notes/version-history/<id>', methods=['GET'])
@token_required
def get_note_version_history(id):
    # Find the note associated with the logged-in user's user ID
    user_note = user_notes_collection.find_one({"note_id": ObjectId(id), "user_id": g.current_user["_id"]})

    if user_note:
        # Find all versions of the note in the notes_collection
        versions = note_history_collection.find({"note_id": ObjectId(id)})

        version_history = []
        for version in versions:
            version_history.append({"note_id":str(version["note_id"]),"note": str(version["note"]), "version": str(version["version"]),
                                     "modified_at":str(version["modified_at"]),"modified_by": str(version["modified_by"])})
        return jsonify(version_history), 200
    else:
        return jsonify({"message": "Note not found or unauthorized"}), 404

if __name__ == '__main__':
    app.run(debug=True)