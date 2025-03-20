from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Titel', validators=[DataRequired()])
    description = TextAreaField('Beschreibung')
    due_date = DateTimeField('Ablaufdatum (z.B.: 2025-04-20 14:00)', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Task speichern')
