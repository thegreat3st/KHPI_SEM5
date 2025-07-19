from flask import Blueprint, render_template, session
import random

lab1_sample_bp = Blueprint('lab1_sample', __name__, template_folder='templates')

# Define lists and ranges for random data
countries = ["France", "Italy", "Turkey", "Indonesia", "Ukraine", "USA", "Norway", "Canada"]
operators = [f"Op{num}" for num in range(1, 6)]

# Generate random tours data
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

@lab1_sample_bp.route("/api/lab1/tours")
def get_tours_sample():
    session['tours_data'] = generate_tour()
    return render_template("public/lab1/templates/tours.html", tours=session['tours_data'])

@lab1_sample_bp.route("/api/lab1/tours/<operator>")
def get_tours_by_operator(operator):
    tours = [tour for tour in session.get('tours_data', []) if tour["operator"] == operator]
    return render_template("public/lab1/templates/tours.html", tours=tours)

@lab1_sample_bp.route("/api/lab1/tours/min_days/<int:n>")
def get_tours_by_days(n):
    tours = [tour for tour in session.get('tours_data', []) if tour["days"] >= n]
    return render_template("public/lab1/templates/tours.html", tours=tours)

@lab1_sample_bp.route("/api/lab1/tours/expensive_turkey_tour")
def get_most_expensive_turkey():
    turkey_tours = [tour for tour in session.get('tours_data', []) if tour["country"] == "Turkey"]
    most_expensive = max(turkey_tours, key=lambda x: x["price"], default=None)
    return render_template("public/lab1/templates/tours.html", tours=[most_expensive] if most_expensive else [])
