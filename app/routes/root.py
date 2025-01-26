from flask import Blueprint, render_template
from app.domains.repositories.map_repository import MapRepository

root_bp = Blueprint("root", __name__)
map_repo = MapRepository()

@root_bp.route('/')
def home():
    geojson, charging_stations = map_repo.get_cached_data()
    return render_template('map.html', geojson=geojson, charging_stations=charging_stations)

@root_bp.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')