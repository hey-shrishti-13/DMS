from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Text                                                         #storing long text

db = SQLAlchemy()                                                                   #creating database object

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    extracted_text = db.Column(db.Text, nullable=True)
