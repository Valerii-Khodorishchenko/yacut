from http import HTTPStatus

from flask import redirect, render_template
from markupsafe import Markup

from . import app
from .forms import URLMapForm
from .models import URLMap


INSTRUCTION = (
    'Вернитесь на главную страницу, попробуйте ещё раз '
    'или введите свой вариант короткой ссылки'
)
NOT_GET_UNIQUE_SHORT_ID = 'Не удалось сгенерировать короткую ссылку.'
ERROR_SHORT_LINK_NOT_FOUND = Markup(
    'Короткой ссылки <span style="color:red">{}</span> не существует.'
)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(form.original_link.data, form.custom_id.data)
    except RuntimeError as e:
        return render_template(
            f'{HTTPStatus.INTERNAL_SERVER_ERROR}.html',
            message=e,
            instruction=INSTRUCTION
        )
    return render_template(
        'index.html',
        form=form,
        short_link=URLMap.get_short_link(url_map.short)
    )


@app.route('/<short>')
def redirect_to_original(short):
    try:
        return redirect(URLMap.get_url_map_by_short(short).original)
    except AttributeError:
        return render_template(
            f'{HTTPStatus.NOT_FOUND}.html',
            error=ERROR_SHORT_LINK_NOT_FOUND.format(
                URLMap.get_short_link(short)
            ),
        ), HTTPStatus.NOT_FOUND
