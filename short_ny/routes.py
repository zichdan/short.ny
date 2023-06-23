from flask import Blueprint, request, redirect, render_template, url_for

from .models import Link
from .extensions import db


shortner = Blueprint('shortner', __name__)


@shortner.route('/<short_url>')
def redirect_to_url(short_url):
    return ""


@shortner.route('/create_link', methods=['POST'])
def create_link():
    orignial_url = request.form['original_url']
    link = Link(orignial_url=orignial_url)
    
    db.session.add(link)
    db.session.commit()
    
    return render_template('link_success.html',
        new_url = link.short_url, orignial_url=link.orignial_url)

@shortner.route('/')
def index():
    return render_template('index.html')


@shortner.route('/analytics')
def analytics():
    return ""


@shortner.errorhandler(404)
def page_not_found(e):
    return "<h1>Page Not Found 404<h1>", 404








