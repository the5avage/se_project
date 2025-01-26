from flask import Blueprint, render_template, jsonify, request
from app.repositories.map_repository import MapRepository
from app.repositories.review_repository import ReviewRepository


map_bp = Blueprint("map", __name__)
map_repo = MapRepository()
review_repo = ReviewRepository()

@map_bp.route('/station_info/<int:station_id>', methods=['GET'])
def station_info(station_id):
    geojson, charging_stations = map_repo.get_cached_data()
    # Find the station with the given ID
    station = next((s for s in charging_stations if s['id'] == station_id), None)
    
    if station:
        return jsonify(station)
    else:
        return jsonify({"error": "Station not found"}), 404
    
    
