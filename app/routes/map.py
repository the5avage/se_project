from flask import Blueprint, render_template, jsonify, request
from app.repositories.map_repository import MapRepository
from app.repositories.review_repository import ReviewRepository
from app import cache

map_bp = Blueprint("map", __name__)
map_repo = MapRepository()
review_repo = ReviewRepository()

def get_cached_data():
    geojson = cache.get('geojson')
    charging_stations = cache.get('charging_stations')
    if not geojson or not charging_stations:
        geojson = map_repo.get_geojson()
        charging_stations = map_repo.get_charging_stations()
        cache.set('geojson', geojson)
        cache.set('charging_stations', charging_stations)
    return geojson, charging_stations

@map_bp.route('/')
def home():
    geojson, charging_stations = get_cached_data()
    return render_template('map.html', geojson=geojson, charging_stations=charging_stations)

@map_bp.route('/station_info/<int:station_id>', methods=['GET'])
def station_info(station_id):
    station = map_repo.get_station_by_id(station_id)
    if not station:
        return jsonify({"error": "Station not found"}), 404

    reviews = review_repo.get_reviews_by_station(station_id)
    average_rating = sum([review['rating'] for review in reviews]) / len(reviews) if reviews else None

    return jsonify({
        "id": station['id'],
        "Name": station['Name'],
        "Address": station['Address'],
        "average_rating": average_rating,
        "reviews": reviews
    })
@map_bp.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')