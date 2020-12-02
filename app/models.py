from .import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from flask_login import UserMixin
from flask_user import UserManager
from datetime import datetime

class User(db.Model,UserMixin):
    __tablename__='users'
    id= db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255),unique = True, index = True)
    password_hash = db.Column(db.String(255))
    comment_id = db.relationship('Comment', backref='user_post', lazy='dynamic')
    role = db.relationship('Role', backref='user', lazy='dynamic')
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String()) 
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
            return check_password_hash(self.password_hash, password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def has_roles(self, *args):
        return set(args).issubset({ role.role_name for role in self.role})

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer,primary_key = True)
    role_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
 class UserRoles(db.Model):
    __tablename__ = 'user_roles'   

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

user_manager = UserManager(app, db, User)
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    content = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post')
    blog_pic_path = db.Column(db.String())
    time_created = db.Column(db.DateTime(), default = datetime.utcnow)
    time_updated = db.Column(db.DateTime(), default = datetime.utcnow, onupdate=datetime.utcnow)

@classmethod
    def get_posts(cls):
        posts = Post.query.all()
        response = []
        response.append(posts)
        return response

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.Text)
    time_created = db.Column(db.DateTime(), default = datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    comment_owner = db.relationship('User',backref='comment')

    def get_comments(self):
        return Comment.query.filter_by(post_id = post.id).order_by(Comment.time_created.desc()).all()

class Subscribe(db.Model):
    __tablename__ = 'subscribed'
    
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String())   

   