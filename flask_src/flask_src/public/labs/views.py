from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    make_response,
    session,
)
import os
import requests
from bs4 import BeautifulSoup as bs
import random


lab_blueprint = Blueprint('lab', __name__, url_prefix='/public', template_folder='templates')

# trips = [
#     {"country": "France", "operator": "Op1", "price": 1200, "days": 7},
#     {"country": "Italy", "operator": "Op1", "price": 1400, "days": 10},
#     {"country": "Turkey", "operator": "Op3", "price": 1000, "days": 6},
#     {"country": "Turkey", "operator": "Op3", "price": 2000, "days": 14},
#     {"country": "Turkey", "operator": "Op1", "price": 7000, "days": 30},
#     {"country": "Indonesia", "operator": "Op4", "price": 4000, "days": 10},
#     {"country": "Ukraine", "operator": "Op5", "price": 3000, "days": 5},
#     {"country": "USA", "operator": "Op4", "price": 5000, "days": 9},
#     {"country": "Norway", "operator": "Op1", "price": 3500, "days": 15},
#     {"country": "Canada", "operator": "Op4", "price": 2000, "days": 14},
#     {"country": "Turkey", "operator": "Op3", "price": 500, "days": 3},
# ]

countries = ["France", "Italy", "Turkey", "Indonesia", "Ukraine", "USA", "Norway", "Canada"]
operators = [f"Op{num}" for num in range(1, 6)]

def generate_tour():
    tours = []
    for _ in range(10):
        days = random.randint(1, 90)
        price_range = (300 * days, 2000 * days)
        tour = {
            "country": random.choice(countries),
            "operator": random.choice(operators),
            "price": random.randint(*price_range),
            "days": days
        }
        tours.append(tour)
    return tours

@lab_blueprint.route('/lab/<int:lab_id>/task')
def lab_task(lab_id):
    img_folder = os.path.join(current_app.static_folder, 'assets', 'img', f'image_for_lab{lab_id}')
    images = sorted([img for img in os.listdir(img_folder) if img.endswith(('.png', '.jpg', '.jpeg', '.gif'))])

    objectives = {
        1: "Отримати базові знання та навички у встановленні фреймворку Flask в \
            віртуальне середовище та в створенні простого Flask-застосунку.",
        2: "Використати шаблонізатор Jinja",
        3: "Пограти в гру Flexbox Froggy",
        4: "Отримати навички роботи з елементами форм, передавати дані з клієнтської \
            частини до серверної та використовувати фреймворк CSS Bootstrap."
    }
    objective = objectives.get(lab_id, "No objective defined for this lab.")
    
    return render_template('public/lab_task_base.html', lab_id=lab_id, images=images, objective=objective)

@lab_blueprint.route('/lab/<int:lab_id>/result')
def lab_result(lab_id):
    images_path = os.path.join(current_app.static_folder, 'assets', 'img', f'image_for_lab{lab_id}_res')
    video_path = os.path.join(current_app.static_folder, 'assets', 'vid', f'lab{lab_id}_video.mp4')  # Define video path
    images = [img for img in os.listdir(images_path) if img.endswith('.png')]  # Only PNGs
    sorted_images = sorted(images, key=lambda x: int(x.split('_')[0][3:]))
    return render_template('public/lab_res_base.html', lab_id=lab_id, images=sorted_images, video_path=video_path if os.path.exists(video_path) else None)

@lab_blueprint.route('/<int:lab_id>/result/to_results')
def lab_to_result(lab_id):
    """Render the detailed results page for each lab with specific trip details and filters."""
    session['tours_data'] = generate_tour()
    trips = session.get('tours_data', [])
    # turkey_trips = [trip for trip in trips if trip["country"].lower() == "turkey"]
    # most_expensive_turkey_trip = max(turkey_trips, key=lambda x: x["price"]) if turkey_trips else None
    return render_template(
        'public/lab_to_result.html',
        lab_id=lab_id,
        trips=trips,
        # most_expensive_turkey_trip=most_expensive_turkey_trip
    )
    

# ================================================================
# =============================  Lab  ============================
# ================================================================

# def fetch_data_from_current_route():
#     response = requests.get(request.url)
#     if response.status_code == 200:
#         soup = bs(response.text, 'html.parser')
#         data = [p.get_text() for p in soup.find_all('p')]
#         return data if data else None
#     return None

# @lab_blueprint.route("/api/tours")
# def yep():
#     data = fetch_data_from_current_route()

#     if not data:
#         no_data_image_url = url_for('static', filename='assets/img/image_sample_lab1/no_data.png')
#         no_data_html = f"""
#             <html>
#                 <body style="text-align: center;">
#                     <img src="{no_data_image_url}" alt="No data image">
#                     <p style="font-size: 20px; color: red;">No Data</p>
#                 </body>
#             </html>
#         """
#         return make_response(no_data_html, 200)

#     return None

@lab_blueprint.route('/<int:lab_id>/result/to_results/page1')
def page1(lab_id):
    """Render the result page for Lab 1, displaying images and trips."""
    return render_template('public/lab1/page1.html', lab_id=lab_id)

@lab_blueprint.route('/<int:lab_id>/result/to_results/page2')
def page2(lab_id):
    """Render the second result page for Lab 1."""
    return render_template('public/lab1/page2.html', lab_id=lab_id)

@lab_blueprint.route('/<int:lab_id>/result/to_results/page3')
def page3(lab_id):
    """Render the third result page for Lab 1."""
    return render_template('public/lab1/page3.html', lab_id=lab_id)

@lab_blueprint.route('/<int:lab_id>/result/to_results/tours/filter')
def get_filtered_tours(lab_id):
    """Display all tours initially, or filter based on operator, minimum days, and country. Turkey 
        most expensive trip and least expensive one, if there is any Turkey trip, also here."""
    trips = session.get('tours_data', [])
    operator = request.args.get('operator')
    country = request.args.get('country')
    days_min = request.args.get('days_min', type=int)
    show_turkey = request.args.get('show_turkey', '')
    
    unique_countries = sorted(set(trip["country"] for trip in trips))

    filtered_trips = trips
    operator_error = None

    if operator or country or days_min is not None:
        if operator:
            filtered_trips = [trip for trip in filtered_trips if trip["operator"].lower() == operator.lower()]
            if len(filtered_trips) == 0:
                operator_error = "No operator found."

        if country:
            filtered_trips = [trip for trip in filtered_trips if trip["country"].lower() == country.lower()]

        if days_min is not None:
            filtered_trips = [trip for trip in filtered_trips if trip["days"] >= days_min]

    turkey_trips = [trip for trip in filtered_trips if trip["country"].lower() == "turkey"]
    most_expensive_turkey_trip = max(turkey_trips, key=lambda x: x["price"]) if turkey_trips else None
    least_expensive_turkey_trip = min(turkey_trips, key=lambda x: x["price"]) if turkey_trips else None

    selected_turkey_trip = (
        most_expensive_turkey_trip if show_turkey == "most_expensive" else least_expensive_turkey_trip
    )

    return render_template(
        'public/lab_to_result.html',
        lab_id=lab_id,
        filtered_trips=filtered_trips,
        trips=trips,
        unique_countries=unique_countries,
        selected_turkey_trip=selected_turkey_trip,
        operator_error=operator_error,
        show_turkey=show_turkey
    )
