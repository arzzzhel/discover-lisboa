from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Modelo de utilizador"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    is_validated = db.Column(db.Boolean, default=False)
    validation_token = db.Column(db.String(255), nullable=True)
    token_expiration = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relação com conteúdos
    contents = db.relationship('Content', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Encriptar password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Content(db.Model):
    """Modelo de conteúdo turístico/gastronómico"""
    __tablename__ = 'contents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # restaurante, museu, monumento, etc.
    media_type = db.Column(db.String(20), nullable=False)  # image, video, audio
    media_filename = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location_name = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Chave estrangeira
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_dict(self):
        """Converter para dicionário (útil para JSON)"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'media_type': self.media_type,
            'media_filename': self.media_filename,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'location_name': self.location_name,
            'created_at': self.created_at.isoformat(),
            'author': self.author.username
        }
    
    def __repr__(self):
        return f'<Content {self.title}>'
