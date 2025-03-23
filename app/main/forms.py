from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length
from flask_babel import _, lazy_gettext as _l

class TaskForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(max=128)])
    description = TextAreaField(_l('Description'), validators=[Length(max=256)])
    due_date = DateTimeField(_l('Due Date'), format='%Y-%m-%dT%H:%M', validators=[DataRequired()])  # HTML5 Datetime-Local
    submit = SubmitField(_l('Submit'))

class EditTaskForm(FlaskForm):  # Separate form for editing
    title = StringField(_l('Title'), validators=[DataRequired(), Length(max=128)])
    description = TextAreaField(_l('Description'), validators=[Length(max=256)])
    due_date = DateTimeField(_l('Due Date'),format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    completed = BooleanField(_l('Completed'))
    submit = SubmitField(_l('Update'))