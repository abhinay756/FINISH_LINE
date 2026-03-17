from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from models import db, User, Project
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# Load config from JSON
with open('config.json', 'r') as f:
    config = json.load(f)['development']
app.config['SECRET_KEY'] = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return send_from_directory('static', 'login.html')

# Serve static files (your HTML/CSS)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user
    user = User(
        name=data['name'],
        email=data['email'],
        role=data['role']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User created successfully',
        'user_id': user.id,
        'role': user.role
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'name': user.name,
            'role': user.role,
            'token': 'fake-jwt-token-123'  # Replace with real JWT
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's projects
    projects = Project.query.filter_by(owner_id=user_id).all()
    
    return jsonify({
        'user': {
            'name': user.name,
            'role': user.role,
            'rating': user.rating
        },
        'projects': [
            {
                'id': p.id,
                'title': p.title,
                'status': p.status,
                'budget': p.budget
            } for p in projects
        ]
    })

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(
        title=data['title'],
        owner_id=data['owner_id'],
        budget=data['budget']
    )
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        'message': 'Project created',
        'project_id': project.id
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
