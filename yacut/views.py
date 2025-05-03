from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .constants import GET_SHORT_ENDPOINT
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(form.original_link.data, form.custom_id.data)
        flash(url_map.get_short_link(), 'success')
    except RuntimeError as e:
        flash(e, 'error')
    return render_template(
        'index.html',
        form=form,
    )


@app.route('/<short>', endpoint=GET_SHORT_ENDPOINT)
def redirect_to_original(short):
    if not (url_map := URLMap.get_or_false(short)):
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
