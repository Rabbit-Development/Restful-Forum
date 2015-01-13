import datetime
from flask import url_for
from restforum import db
from passlib.apps import custom_app_context as pwd_context


class Topic(Document):
    title = db.StringField(max_length=255, required=True)
    description = db.StringField(required=True)
    posts = db.ListField(db.EmbeddedDocumentField('Post'))

class Post(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    body = db.StringField()
    image_path = StringField()
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    author = ReferenceField(User, reverse_delete_rule=CASCADE)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True
    }

class User(Document):
    email = StringField(required=True)
    username = StringField(max_length=50, required=True)
    password = StringField(required=True)

    def hash_password(password):
        return pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def __init__(self, email, password, username):
        self.email = email
        self.password = hash_password(password)
        self.username = username

class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    author = ReferenceField(User, reverse_delete_rule=CASCADE)