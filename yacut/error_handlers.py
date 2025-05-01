from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invslid_api_usage(error):
    if error.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        db.session.rollback()
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    return (
        render_template(f'{HTTPStatus.NOT_FOUND}.html'),
        HTTPStatus.NOT_FOUND
    )
