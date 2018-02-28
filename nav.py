from flask import Blueprint, request, render_template, redirect
bp = Blueprint('nav', __name__)

@bp.route('/privacy')
def privacy():
	return render_template('privacy.html')

@bp.route('/about')
def about():
	return render_template('about.html')