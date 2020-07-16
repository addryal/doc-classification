import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

#Configuration setup
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:EmmanueL1@localhost/document_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
UPLOAD_FOLDER = os.path.join(os.getcwd(), "text_files")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


toolbar = DebugToolbarExtension(app)

#Linking and registering the database
db = SQLAlchemy(app)
Migrate(app,db)

#Blueprint registration
from project.document.views import doc_blueprint
app.register_blueprint(doc_blueprint,url_prefix='/document')
