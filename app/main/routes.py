from app.main.forms import TaskForm
from app.models import Task
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from datetime import datetime

# Dashboard (Tasks anzeigen)
@bp.route('/dashboard')
@login_required
def dashboard():
    tasks = current_user.tasks.order_by(Task.due_date.asc()).all()
    return render_template('dashboard.html', tasks=tasks)

# Task erstellen
@bp.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            author=current_user
        )
        db.session.add(task)
        db.session.commit()
        flash('Task erfolgreich erstellt.')
        return redirect(url_for('main.dashboard'))
    return render_template('create_task.html', form=form)

# Task bearbeiten
@bp.route('/edit_task/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.author != current_user:
        flash('Keine Berechtigung!')
        return redirect(url_for('main.dashboard'))
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        db.session.commit()
        flash('Task aktualisiert.')
        return redirect(url_for('main.dashboard'))
    return render_template('edit_task.html', form=form, task=task)

# Task löschen
@bp.route('/delete_task/<int:id>', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.author != current_user:
        flash('Keine Berechtigung!')
        return redirect(url_for('main.dashboard'))
    db.session.delete(task)
    db.session.commit()
    flash('Task gelöscht.')
    return redirect(url_for('main.dashboard'))
