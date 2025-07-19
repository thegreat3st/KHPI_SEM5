from flask import Blueprint, render_template, session
import random

lab2_sample_bp = Blueprint('lab2_sample', __name__, template_folder='templates')

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

@lab2_sample_bp.route("/api/lab2/tours")
def get_tours_sample():
    session['tours_data'] = generate_tour()
    return render_template("public/lab2/templates/tours.html", tours=session['tours_data'])

@lab2_sample_bp.route("/api/lab2/tours/<operator>")
def get_tours_by_operator(operator):
    return render_template("public/lab2/templates/tours.html", tours=session.get('tours_data', []), filter_operator=operator)

@lab2_sample_bp.route("/api/lab2/tours/min_days/<int:n>")
def get_tours_by_days(n):
    return render_template("public/lab2/templates/tours.html", tours=session.get('tours_data', []), min_days=n)

@lab2_sample_bp.route("/api/lab2/tours/expensive_turkey_tour")
def get_most_expensive_turkey():
    return render_template("public/lab2/templates/tours.html", tours=session.get('tours_data', []), expensive_turkey=True)
