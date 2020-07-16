from flask_wtf import Form
from wtforms import StringField,SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email

class DocumentUploadForm(Form):
    doc_class = StringField('Document Class', validators=[DataRequired()])
    document = FileField('Document', validators=[FileRequired(), FileAllowed(['txt', 'xlsx'], 'Text files only')])
    submit = SubmitField('Add document class')