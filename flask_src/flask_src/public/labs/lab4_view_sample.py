from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from flask_src.config import THEMES_WITH_DESCRIPTIONS
import random

lab4_sample_bp = Blueprint('lab4_sample', __name__, template_folder='templates', url_prefix='/gallow')

@lab4_sample_bp.route('/', methods=['GET', 'POST'])
def select_theme():
    if request.method == 'POST':
        data = request.get_json()
        theme = data.get("theme")
        selection_mode = data.get("selection_mode")
        word = data.get("word")

        # Extract theme data
        theme_data = next((item for item in THEMES_WITH_DESCRIPTIONS if item['theme'] == theme), None)
        if theme_data:
            session['theme'] = theme
            session['theme_description'] = theme_data['description']
            session['theme_words'] = theme_data['words']

            if selection_mode == "random":
                chosen_word = random.choice(theme_data['words']).upper()
                session['chosen_word'] = chosen_word
            elif selection_mode == "manual" and word:
                session['chosen_word'] = word.upper()

            # Redirect to the game page
            return jsonify(success=True, redirect_url=url_for('public.lab4_sample.play'))

        return jsonify(success=True)

    themes = [item['theme'] for item in THEMES_WITH_DESCRIPTIONS]
    theme_descriptions = {item['theme']: item['description'] for item in THEMES_WITH_DESCRIPTIONS}

    return render_template(
        'public/lab4/templates/select_theme.html',
        themes=themes,
        theme_descriptions=theme_descriptions
    )

@lab4_sample_bp.route('/play', methods=['GET'])
def play():
    word = session.get('chosen_word')
    theme = session.get('theme')

    if not word or not theme:
        return redirect(url_for('lab4_sample.select_theme'))

    placeholder = "_" * len(word)
    return render_template('public/lab4/templates/play.html', word=word, placeholder=placeholder, theme=theme)

@lab4_sample_bp.route('/end', methods=['POST'])
def end_game():
    """Clear session data after game ends."""
    session.pop('chosen_word', None)
    session.pop('theme', None)
    session.pop('theme_description', None)
    session.pop('theme_words', None)
    return jsonify(success=True)
