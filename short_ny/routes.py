from flask import Blueprint, request, redirect, render_template, url_for,jsonify 

from .models import Link
from .extensions import db


shortner = Blueprint('shortner', __name__)


@shortner.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    link.views = link.views + 1
    
    db.session.commit()
    
    return redirect(link.original_url)



@shortner.route('/create_link', methods=['POST'])
def create_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    
    db.session.add(link)
    db.session.commit()
    
    return render_template('link_success.html',
        new_url = link.short_url, original_url=link.original_url)

@shortner.route('/')
def index():
    return render_template('index.html')


@shortner.route('/analytics')
def analytics():
    links = Link.query.all()

    return render_template('analytics.html', links=links)

# @shortner.route('/analytics')
# def analytics():
#     link = Link.query.all()
#     links = []

#     for l in link:
#         views = str(l.views) 
#         short_url = str(l.short_url)
#         url = str(l.original_url)

#         data = {
#             'views': views,
#             'short_url' : short_url,
#             'url' : url
#         }
#         links.append(data)
        
#     print (links)
#     return jsonify({'links': links})


@shortner.errorhandler(404)
def page_not_found(e):
    return "<h1>Page Not Found 404<h1>", 404








