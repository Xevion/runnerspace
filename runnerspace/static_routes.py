from flask import Blueprint, redirect, render_template, url_for, request

blueprint = Blueprint('static', __name__)


@blueprint.route('/about')
def about():
    return render_template('pages/about.html')


@blueprint.route('/terms_of_service')
def tos():
    return render_template('static/tos.html')


@blueprint.route('/privacy')
def privacy():
    return render_template('static/privacy.html')


@blueprint.route('/license')
def license():
    return render_template('static/license.html')
