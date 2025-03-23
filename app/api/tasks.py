import sqlalchemy as sa
from flask import jsonify, request, url_for # url_for keeps being imported
from app import db
from app.models import Task
from app.api import bp
from app.api.auth import token_auth
#from app.api.errors import bad_request #Not needed.

@bp.route('/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    query = token_auth.current_user().tasks.select().order_by(Task.due_date.asc())
    tasks = db.paginate(query, page=page, per_page=per_page, error_out=False)

    data = {
        'items': [item.to_dict() for item in tasks.items],
        '_meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': tasks.pages,
            'total_items': tasks.total
        },
        '_links': {  # This section is fine; it refers to get_tasks itself
            'self': url_for('api.get_tasks', page=page, per_page=per_page),
            'next': url_for('api.get_tasks', page=page + 1, per_page=per_page)
                    if tasks.has_next else None,
            'prev': url_for('api.get_tasks', page=page - 1, per_page=per_page)
                    if tasks.has_prev else None
        }
    }
    return jsonify(data)