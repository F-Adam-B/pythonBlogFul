from blog._init_ import app
from flask import Markup
import mistune as md


@app.template_filter()
def markdown(text):
    return Markup(md.markdown(text, escape=True))


@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    # formats the date correctly
    return date.strftime(format)
