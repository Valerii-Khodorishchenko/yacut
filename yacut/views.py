import random
import string
from urllib.parse import unquote

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    short = ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length)
    )
    if URLMap.query.filter_by(short=short).first() is not None:
        short = get_unique_short_id()
    return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
        if URLMap.query.filter_by(short=short).first() is not None:
            return render_template('index.html', form=form)
        url_map = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        flash(unquote(url_for(
            'redirect_to_short', short=short, _external=True
        )))
    return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_to_short(short):
    if (link := URLMap.query.filter_by(short=short).first()) is not None:
        return redirect(link.original)
    abort(404)
