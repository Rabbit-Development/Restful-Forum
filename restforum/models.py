import datetime
from flask import url_for
from restforum import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    username = db.StringField(max_length=50, required=True)
    password = db.StringField(required=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def hash_password(password):
        return pwd_context.encrypt(password)

class Topic(db.Document):
    title = db.StringField(max_length=255, required=True)
    description = db.StringField(required=True)
    restricted = db.BooleanField(required=True)
    posts = db.ListField(db.EmbeddedDocumentField('Post'))
    subtopics = db.ListField(db.EmbeddedDocumentField('Topic'))

class Post(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    body = db.StringField()
    image_path = db.StringField()
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    author = db.ReferenceField(User)

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True
    }

class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    author = db.ReferenceField(User)