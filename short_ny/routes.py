from flask import Blueprint, flash, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from .extensions import db, cache, limiter
from .models import  Link
import random, string, requests, io, qrcode


shortner = Blueprint('shortner', __name__)



def generate_short_link(length=5):
    chars = string.ascii_letters + string.digits
    short_link = ''.join(random.choice(chars) for _ in range(length))
    return short_link


def generate_qr_code(link):
    image = qrcode.make(link)
    image_io = io.BytesIO()
    image.save(image_io, 'PNG')
    image_io.seek(0)
    return image_io


@shortner.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@shortner.errorhandler(403)
def error_404(error):
    return render_template('403.html'), 403


@shortner.route('/', methods=['GET', 'POST'])
@limiter.limit('10/minutes')
def index():
    if request.method == 'POST':
        long_link = request.form['long_link']
        custom_path = request.form['custom_path'] or None
        long_link_exists = Link.query.filter_by(user_id=current_user.id).filter_by(long_link=long_link).first()

        if requests.get(long_link).status_code != 200:
            return render_template('404.html')

        elif long_link_exists:
            flash ('This link has already been shortened.')
            return redirect(url_for('shortner.dashboard'))

        elif custom_path:
            path_exists = Link.query.filter_by(custom_path=custom_path).first()
            if path_exists:
                flash ('That custom path is taken. Please try another.')
                return redirect(url_for('shortner.index'))
            short_link = custom_path

        elif long_link[:4] != 'http':
            long_link = 'http://' + long_link
        
        else:
            while True:
                short_link = generate_short_link()
                short_link_exists = Link.query.filter_by(short_link=short_link).first()
                if not short_link_exists:
                    break
        
        link = Link(long_link=long_link, short_link=short_link, custom_path=custom_path, user_id=current_user.id)
        db.session.add(link)
        db.session.commit()
        return redirect(url_for('shortner.dashboard'))
    
    return render_template('index.html')


@shortner.route('/about')
def about():
    return render_template('about.html')


@shortner.route('/dashboard')
@login_required
def dashboard():
    links = Link.query.filter_by(user_id=current_user.id).order_by(Link.created_at.desc()).all()
    host = request.host_url
    return render_template('dashboard.html', links=links, host=host)


@shortner.route('/history')
@login_required
def history():
    links = Link.query.filter_by(user_id=current_user.id).order_by(Link.created_at.desc()).all()
    host = request.host_url
    return render_template('history.html', links=links, host=host)


@shortner.route('/<short_link>')
@cache.cached(timeout=30)
def redirect_link(short_link):
    link = Link.query.filter_by(short_link=short_link).first()
    if link:
        link.clicks += 1
        db.session.commit()
        return redirect(link.long_link)
    else:
        return render_template('404.html')


@shortner.route('/<short_link>/qr_code')
@login_required
@cache.cached(timeout=30)
@limiter.limit('10/minutes')
def generate_qr_code_link(short_link):
    link = Link.query.filter_by(user_id=current_user.id).filter_by(short_link=short_link).first()

    if link:
        image_io = generate_qr_code(request.host_url + link.short_link)
        return image_io.getvalue(), 200, {'Content-Type': 'image/png'}
    
    return render_template('404.html')


@shortner.route('/<short_link>/delete')
@login_required
def delete(short_link):
    link = Link.query.filter_by(user_id=current_user.id).filter_by(short_link=short_link).first()

    if link:
        db.session.delete(link)
        db.session.commit()
        return redirect(url_for('shortner.dashboard'))
    
    return render_template('404.html')


@shortner.route('/<short_link>/edit', methods=['GET', 'POST'])
@login_required
@limiter.limit('10/minutes')
def update(short_link):
    link = Link.query.filter_by(user_id=current_user.id).filter_by(short_link=short_link).first()
    host = request.host_url
    if link:
        if request.method == 'POST':
            custom_path = request.form['custom_path']
            if custom_path:
                link_exists = Link.query.filter_by(custom_path=custom_path).first()
                if link_exists:
                    flash ('That custom path already exists. Please try another.')
                    return redirect(url_for('shortner.update', short_link=short_link))
                link.custom_path = custom_path
                link.short_link = custom_path
            db.session.commit()
            return redirect(url_for('shortner.dashboard'))
        return render_template('edit.html', link=link, host=host)
    return render_template('404.html')


@shortner.route('/<short_link>/analytics')
@login_required
def analytics(short_link):
    link = Link.query.filter_by(user_id=current_user.id).filter_by(short_link=short_link).first()
    host = request.host_url
    if link:
        return render_template('analytics.html', link=link, host=host)
    return render_template('404.html')

