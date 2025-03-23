from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField, TimeField  # TimeField hinzugefügt
from wtforms.validators import DataRequired, Length, Optional  # Optional hinzugefügt
from flask_babel import _, lazy_gettext as _l

class TaskForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(max=128)])
    description = TextAreaField(_l('Description'), validators=[Length(max=256)])
    due_date = DateField(_l('Due Date'), validators=[DataRequired()])  # DateField
    due_time = TimeField(_l('Due Time'), validators=[Optional()])  # TimeField, Optional
    submit = SubmitField(_l('Submit'))

class EditTaskForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(), Length(max=128)])
    description = TextAreaField(_l('Description'), validators=[Length(max=256)])
    due_date = DateField(_l('Due Date'), validators=[DataRequired()])  # DateField
    due_time = TimeField(_l('Due Time'), validators=[Optional()]) # TimeField, Optional
    completed = BooleanField(_l('Completed'))
    submit = SubmitField(_l('Update'))