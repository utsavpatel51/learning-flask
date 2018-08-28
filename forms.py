from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length
class SignUpForm(Form):
    f_name=StringField('First Name',validators=[DataRequired("Enter a First Name")])
    l_name=StringField('Last Name',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired("Enter a Email"),Email("Enter a Valid Email")])
    passwd=StringField('Password',validators=[DataRequired(),Length(min=8,message="Enter atleast 8 char")])
    submit=SubmitField('Sign Up')
