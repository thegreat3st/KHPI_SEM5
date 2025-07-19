# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)
from flask_login import login_required, login_user, logout_user
import os
import json
from markdown import markdown
from flask_src.extensions import login_manager
from flask_src.public.forms import LoginForm
from flask_src.user.forms import RegisterForm
from flask_src.user.models import User
from flask_src.utils import flash_errors

# ======== LABs views file ========
from flask_src.public.labs.views import lab_blueprint
from flask_src.public.labs.lab1_view_sample import lab1_sample_bp
from flask_src.public.labs.lab2_view_sample import lab2_sample_bp
from flask_src.public.labs.lab4_view_sample import lab4_sample_bp
# =================================
from environs import Env

env = Env()
env.read_env()

path = env.str("PROJECT_PATH")

blueprint = Blueprint("public", __name__, static_folder="templates")
blueprint.register_blueprint(lab_blueprint)
blueprint.register_blueprint(lab1_sample_bp)
blueprint.register_blueprint(lab2_sample_bp)
blueprint.register_blueprint(lab4_sample_bp)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))

# ================================================================
# ============================  Home  ============================
# ================================================================

@blueprint.route('/')
def home():
    return render_template('public/home.html')

# Recursive function to create structured data with indentation levels
def get_directory_structure(rootdir, level=0):
    structure = []
    for item in sorted(os.listdir(rootdir)):
        item_path = os.path.join(rootdir, item)
        if os.path.isdir(item_path):
            structure.append({
                "name": item,
                "type": "folder",
                "level": level,
                "children": get_directory_structure(item_path, level + 1)
            })
        else:
            structure.append({
                "name": item,
                "type": "file",
                "path": item_path,
                "level": level
            })
    return structure

@blueprint.route('/tree', methods=['GET'])
def tree_view():
    root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '/Users/thegreatest/PyFolder2/Flask_Khpi/flask_src'))
    directory_structure = get_directory_structure(root_directory)
    return render_template("public/tree.html", dir_structure=directory_structure)

@blueprint.route('/api/file_content', methods=['GET'])
def get_file_content():
    filepath = request.args.get('path')
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)})


# ================================================================
# ============================  Labs  ============================
# ================================================================

@blueprint.route('/labs')
def labs():
    """Labs page showing tasks and results for each lab."""
    return render_template('public/labs.html')


# ================================================================
# ============================  Auth  ============================
# ================================================================

# @blueprint.route("/", methods=["GET", "POST"])
# def home():
#     """Home page."""
#     form = LoginForm(request.form)
#     current_app.logger.info("Hello from the home page!")
    # # Handle logging in
    # if request.method == "POST":
    #     if form.validate_on_submit():
    #         login_user(form.user)
    #         flash("You are logged in.", "success")
    #         redirect_url = request.args.get("next") or url_for("user.members")
    #         return redirect(redirect_url)
    #     else:
    #         flash_errors(form)
    # return render_template("public/home.html", form=form)


# @blueprint.route("/logout/")
# @login_required
# def logout():
#     """Logout."""
#     logout_user()
#     flash("You are logged out.", "info")
#     return redirect(url_for("public.home"))


# @blueprint.route("/register/", methods=["GET", "POST"])
# def register():
#     """Register new user."""
#     form = RegisterForm(request.form)
#     if form.validate_on_submit():
#         User.create(
#             username=form.username.data,
#             email=form.email.data,
#             password=form.password.data,
#             active=True,
#         )
#         flash("Thank you for registering. You can now log in.", "success")
#         return redirect(url_for("public.home"))
#     else:
#         flash_errors(form)
#     return render_template("public/register.html", form=form)
