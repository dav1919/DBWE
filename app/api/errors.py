from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from app.api import bp #Needs to stay connected with bp
from flask import jsonify, make_response #Added

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload) #Jsonify added to return Json Object
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(400, message)

@bp.errorhandler(HTTPException)
def handle_exception(e):
    return error_response(e.code)