from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddForm(FlaskForm):

    name = StringField('Name of Document Class:')
    function =  StringField('Name of Document Class:')
    pup_id = IntegerField("Id of Puppy: ")
    submit = SubmitField('Add Owner')
