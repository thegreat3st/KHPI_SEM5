# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_src.public.labs import lab1_view_sample as lab

def create_app(config_object="flask_src.settings"):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_object)
    
    register_errorhandlers(app)
    register_blueprints(app)
    # other regs...
    return app

def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(404)
    def page_not_found(e):
        """Handle 404 errors with custom template."""
        return render_template("public/lab1/templates/lab1_404.html"), 404

    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(lab.lab1_sample_bp)
    return None
