from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo
from app.models import logo
import requests

class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    remember_me=BooleanField("Remember Me")
    submit=SubmitField("Login")
    matchid=StringField("match")
    matchinfo=StringField("mat")

class RegisterForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    password2=PasswordField("Retype Password",validators=[DataRequired(),EqualTo('password')])
    email=StringField("Email",validators=[DataRequired(),Email()])
    id=IntegerField("Player ID",validators=[DataRequired()])
    submit=SubmitField("Register")

    def validate_email(self,email):
        user=logo.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("This email is already registered")

    def validate_id(self,id):
        user=logo.query.filter_by(id=id.data).first()
        if user is not None:
            raise ValidationError("This id is already registered")


        aid=0
        list1=[]
        re1=requests.get(f"https://api.opendota.com/api/players/{id.data}")
        js1=re1.json()
        print(js1)
        for key,values in js1.items():
            if key=='profile':
                list1.append(values)

        print(list1)
        for i in list1:
            if i['account_id']:
                aid=i['account_id']


        print(aid)

        if id.data != aid:
            raise ValidationError("Please enter a valid PlayerID")


class matchbar(FlaskForm):
    matchinfo=SubmitField("GETMATCH")
    matchid=IntegerField("Match ID",validators=[DataRequired()])

    def validate_matchid(self,matchid):

        req=requests.get(f"https://api.opendota.com/api/matches/{matchid.data}")
        js=req.json()
        print(js)
        for key,values in js.items():
            if key=="error":
                raise ValidationError("Please enter a valid MatchID")
