from flask import Blueprint, render_template, request
from ...controllers.api.errors import error_response as api_error_response

errors = Blueprint("errors", __name__)

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@errors.app_errorhandler(403)
def forbidden_error(error):
    if wants_json_response():
        return api_error_response(403)
    context = {
        'error_code': '403',
        'heading': 'Forbidden',
        'description': 'Sorry but you are not allowed for dowing this action .'
    }
    return render_template('errors/error.html', **context), 403


@errors.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    context = {
        'error_code': '404',
        'heading': 'Page Not Found',
        'description': 'The page you are looking for might have been removed had its name changed or is temporarily unavailable .'
    }
    return render_template('errors/error.html', **context), 404


@errors.app_errorhandler(405)
def method_not_allawed_error(error):
    if wants_json_response():
        return api_error_response(405)
    context = {
        'error_code': '405',
        'heading': 'Method Not Allawed',
        'description': 'The method is not allowed for the requested URL.'
    }
    return render_template('errors/error.html', **context), 405


@errors.app_errorhandler(410)
def gone_error(error):
    if wants_json_response():
        return api_error_response(410)
    context = {
        'error_code': '410',
        'heading': 'Gone',
        'description': 'The above error occurred while the Web Server was processing your request .'
    }
    return render_template('errors/error.html', **context), 410


@errors.app_errorhandler(500)
def internal_error(error):
    if wants_json_response():
        return api_error_response(500)
    context = {
        'error_code': '500',
        'heading': 'Internal Server Error',
        'description': 'An unexpected error seems to have occurred try to refresh the page .'
    }
    return render_template('errors/error.html', **context), 500
