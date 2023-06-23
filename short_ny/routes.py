from flask import Blueprint, request, redirect, render_template, url_for


shortner = Blueprint('shortner', __name__)



@shortner.route('/')
def index():
    return render_template('index.html')


@shortner.route('/<short_url>')
def redirect_to_long_url(short_url):
    return redirect(url_for('long_url.redirect_to_long_url', long_url=short_url))


@shortner.route('/create_link', method=['POST'])
def create_link():
    return  ""

@shortner.route('/analytics')
def analytics():
    return ""


# @shortner.errorhandler(403)
# def page_not_found():
#     return ""


@shortner.errorhandler(404)
def page_not_found(e):
    return "<h1>Page Not Found 404<h1>", 404








