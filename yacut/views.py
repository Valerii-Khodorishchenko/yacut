from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_link=URLMap.create(
                form.original_link.data, form.custom_id.data, do_validate=False
            ).get_short_link()
        )
    except (RuntimeError, ValueError) as e:
        flash(str(e))
        return render_template(
            'index.html',
            form=form,
        )


@app.route('/<short>')
def redirect_to_original(short):
    if not (url_map := URLMap.get(short)):
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
