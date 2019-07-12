from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean(50), default=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    createdtime = db.Column(db.DateTime(datetime.utcnow), nullable=False)

class postschema(ma.Schema):
    class Meta:
        fields = ('id', 'status', 'title', 'body', 'createdtime')

post_schema = postschema(strict=True)
posts_schema = postschema(many=True, strict=True)

@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    all_posts = post.query.all()
    result = posts_schema.dump(all_posts)
    return jsonify(result.data)

@app.route('/api/post/<id>', methods=['GET'])
def get_post(id):
    posts = post.query.get(id)
    return post_schema.jsonify(posts)

@app.route('/api/new-post', methods=['POST'])
def new_post():
    data = request.get_json()
    title = data['title']
    body = data['body']
    Post= post(title=title, body=body, status=True, createdtime=datetime.utcnow())
    db.session.add(Post)
    db.session.commit()
    return jsonify({
        'message': 'Post created Successfully'
        })

@app.route('/api/post/<id>', methods=['PUT'])
def update_post(id):
    Post = post.query.get(id)

    data = request.get_json()
    title = data['title']
    body = data['body']
    status = data['status']
    createdtime = datetime.utcnow()

    Post.title = title
    Post.body = body
    Post.status = status
    Post.createdtime = createdtime

    db.session.commit()

    return post_schema.jsonify(Post)

@app.route('/api/post/<id>', methods=['DELETE'])
def delete_post(id):
    posts = post.query.get(id)
    db.session.delete(posts)
    db.session.commit()
    return post_schema.jsonify(posts)

    return ''

if __name__ == '__main__':
    app.run(debug=True)