from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired


class CalculationForm(FlaskForm):
    start1 = FloatField('Start Point Latitude', validators=[DataRequired()])
    start2 = FloatField('Start Point Longitude', validators=[DataRequired()])
    submit = SubmitField('Find')
