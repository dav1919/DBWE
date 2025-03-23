from datetime import datetime, date, time, timezone  # time hinzugefügt
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from flask_babel import _
import sqlalchemy as sa
from app import get_locale
from app import db
from app.main.forms import TaskForm, EditTaskForm
from app.models import User, Task
from app.main import bp

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
    g.locale = str(get_locale()) # Diese Zeile ist wichtig!

def create_task(form):
    """Erstellt einen neuen Task."""
    due_datetime = datetime.combine(form.due_date.data,
                                    form.due_time.data if form.due_time.data else time(0,0))
    task = Task(title=form.title.data, description=form.description.data,
                due_date=due_datetime, user=current_user)
    db.session.add(task)
    db.session.commit()
    return task


def update_task(task, form):
    """Aktualisiert einen vorhandenen Task."""
    due_datetime = datetime.combine(form.due_date.data,
                                    form.due_time.data if form.due_time.data else time(0,0))

    task.title = form.title.data
    task.description = form.description.data
    task.due_date = due_datetime
    task.completed = form.completed.data
    db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TaskForm()
    if form.validate_on_submit():
        create_task(form) # Funktionsaufruf
        flash(_('Your task has been created!'))
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    query = current_user.tasks.select().order_by(Task.due_date.asc())
    tasks = db.paginate(query, page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False)
    next_url = url_for('main.index', page=tasks.next_num) \
        if tasks.has_next else None
    prev_url = url_for('main.index', page=tasks.prev_num) \
        if tasks.has_prev else None

    return render_template('index.html', title=_('Home'), form=form,
                            tasks=tasks.items, next_url=next_url,
                            prev_url=prev_url)


@bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    if task.user != current_user:
        flash(_('You cannot edit this task.'))
        return redirect(url_for('main.index'))

    form = EditTaskForm(obj=task)  # Vorbelegen der Formulardaten
    if form.validate_on_submit():
        update_task(task, form)
        flash(_('Your task has been updated!'))
        return redirect(url_for('main.index'))

    return render_template('edit_task.html', title=_('Edit Task'), form=form, task=task)

@bp.route('/task/<int:task_id>/complete', methods=['POST'])
@login_required
def complete_task(task_id):
      task = db.get_or_404(Task, task_id)
      if task.user != current_user:
          flash(_('You cannot complete this task.'))
          return redirect(url_for('main.index'))
  
      task.completed = not task.completed  # Toggle den Status
      db.session.commit()
      flash(_('Task status updated.'))
      return redirect(url_for('main.index'))
  
@bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
      task = db.get_or_404(Task, task_id)
      if task.user != current_user:
          flash(_('You cannot delete this task.'))
          return redirect(url_for('main.index'))
  
      db.session.delete(task)
      db.session.commit()
      flash(_('Task deleted.'))
      return redirect(url_for('main.index'))
  
  
@bp.route('/user/<username>')
@login_required
def user(username):
      user = db.first_or_404(sa.select(User).where(User.username == username))
      #Keine Posts, darum auch tasks anzeigen:
      page = request.args.get('page', 1, type=int)
      query = user.tasks.select().order_by(Task.due_date.asc())  # Nach Fälligkeitsdatum sortieren
      tasks = db.paginate(query, page=page,
                          per_page=current_app.config['POSTS_PER_PAGE'],
                          error_out=False)
      next_url = url_for('main.user', username=user.username,
                           page=tasks.next_num) if tasks.has_next else None
      prev_url = url_for('main.user', username=user.username,
                           page=tasks.prev_num) if tasks.has_prev else None
      return render_template('user.html', user=user, tasks=tasks.items,
                             next_url=next_url, prev_url=prev_url)