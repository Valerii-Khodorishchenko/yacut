import random
import string
from urllib.parse import unquote

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


INSTRUCTION = '''Вернитесь на главную страницу, попробуйте ещё раз
    или введите свой вариант короткой ссылки'''
NOT_GET_UNIQUE_SHORT_ID = 'Не удалось сгенерировать короткую ссылку.'


def get_unique_short_id(length=6, attempts=10):
    charset = string.ascii_letters + string.digits
    for _ in range(attempts):
        short = ''.join(random.choices(charset, k=length))
        if URLMap.query.filter_by(short=short).first() is None:
            return short
        raise RuntimeError(NOT_GET_UNIQUE_SHORT_ID)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        try:
            short = form.custom_id.data or get_unique_short_id()
        except RuntimeError as f:
            return render_template(
                '500.html', message=f, instruction=INSTRUCTION
            )
        url_map = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        flash(unquote(url_for(
            'redirect_to_original', short=short, _external=True
        )))
    return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_to_original(short):
    flash(unquote(url_for(
        'redirect_to_original', short=short, _external=True
    )))
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
