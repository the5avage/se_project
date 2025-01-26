from flask import render_template, jsonify
from app.repositories.map_repository import MapRepository
from app.repositories.review_repository import ReviewRepository
from app import cache

map_repo = MapRepository()
review_repo = ReviewRepository()

def get_cached_data():
    """
    Fetches GeoJSON and charging stations data from cache or repository.
    """
    geojson = cache.get('geojson')
    charging_stations = cache.get('charging_stations')
    if not geojson or not charging_stations:
        geojson = map_repo.get_geojson()
        charging_stations = map_repo.get_charging_stations()
        cache.set('geojson', geojson)
        cache.set('charging_stations', charging_stations)
    return geojson, charging_stations

def handle_home_event():
    """
    Handles the home event, rendering the map with geojson and charging station data.
    """
    geojson, charging_stations = get_cached_data()
    return render_template('map.html', geojson=geojson, charging_stations=charging_stations)

def handle_station_info_event(station_id):
    """
    Handles the station info event, returning details about a specific charging station.
    """
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

def handle_contact_event():
    """
    Handles the contact event, rendering the contact page.
    """
    return render_template('contact.html')
