# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/29 16:13 
# @Author : lijun7 
# @File : test.py
# @desc :
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
