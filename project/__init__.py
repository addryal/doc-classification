import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


UPLOAD_FOLDER = os.path.join(os.getcwd(), "text_files")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:EmmanueL1@localhost/document_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.debug = True

toolbar = DebugToolbarExtension(app)
db = SQLAlchemy()
db.init_app(app)


from project.document.views import doc_blueprint
app.register_blueprint(doc_blueprint,url_prefix='/document')
