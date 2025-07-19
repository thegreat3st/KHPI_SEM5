# -*- coding: utf-8 -*-
from flask.cli import FlaskGroup
from flask_src.app import create_app
from flask_src.extensions import db

app = create_app()
cli = FlaskGroup(create_app=create_app)

if __name__ == "__main__":
    cli()
