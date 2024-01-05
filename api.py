"""A RESTful CRUD API to store blog posts with JWT authorization.

Viewing posts is public but editing/adding requires authorization."""
from datetime import datetime
import dotenv
from flask import Flask, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
import os
import sqlalchemy as sa
import uuid

# load environment variables from .env file
dotenv.load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sa.URL.create(
    drivername='postgresql+pg8000',
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWD'),
    database=os.getenv('DB_NAME'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['BCRYPT_LOG_ROUNDS'] = 12

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class User(db.Model):
    """Class representing application users."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)


class Blog(db.Model):
    """Class representing a blog post."""
    id = db.Column(
        db.String(36),
        primary_key=True,
        default=str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/api/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.json

        # Validate that password and confirm_password fields match in the form
        if data['password'] != data['confirm_password']:
            return jsonify(message='Passwords do not match'), 400

        # data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(
            data['password']
        ).decode('utf-8')
        new_user = User(
            username=data['username'], password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message='User registered successfully'), 201


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(
            user.password_hash, data['password']
        ):
            access_token = create_access_token(identity=data['username'])
            print(access_token)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify(message='Invalid credentials'), 401


@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    blog_list = []
    for blog in blogs:
        blog_list.append(
            {
                'id': blog.id,
                'title': blog.title,
                'content': blog.content,
                'author': blog.author,
                'timestamp': blog.timestamp,
            }
        )
    return jsonify(blogs=blog_list)


@app.route('/api/blogs/<string:id>', methods=['GET'])
def get_blog(id):
    blog = Blog.query.get(id)
    if blog:
        blog_data = {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'author': blog.author,
            'timestamp': blog.timestamp,
        }
        return jsonify(blog=blog_data)
    else:
        return jsonify(message='Blog not found'), 404


@app.route('/api/blogs', methods=['POST'])
@jwt_required()
def create_blog():
    current_user = get_jwt_identity()
    print(current_user)

    data = request.get_json()
    print(data)

    new_blog = Blog(
        title=data['title'], content=data['content'], author=current_user
    )
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(message='Blog created successfully'), 201


@app.route('/api/blogs/<string:id>', methods=['PUT'])
@jwt_required()
def update_blog(id):
    current_user = get_jwt_identity()
    blog = Blog.query.get(id)
    if blog and blog.author == current_user:
        data = request.get_json()
        blog.title = data['title']
        blog.content = data['content']
        db.session.commit()
        return jsonify(message='Blog updated successfully'), 200
    else:
        return jsonify(message='Blog not found or unauthorized'), 404


@app.route('/api/blogs/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_blog(id):
    current_user = get_jwt_identity()
    blog = Blog.query.get(id)
    if blog and blog.author == current_user:
        db.session.delete(blog)
        db.session.commit()
        return jsonify(message='Blog deleted successfully'), 200
    else:
        return jsonify(message='Blog not found or unauthorized'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
