from flask import Blueprint, request,  render_template
from app.repositories.map_repository import MapRepository

search_bp = Blueprint('search', __name__)
map_repo = MapRepository()

@search_bp.route('/charging_station', methods=['POST'])
def search_charging_station():
    query = request.form.get('query', '').lower() 
    geojson, charging_stations = map_repo.get_cached_data()
    results = [station for station in charging_stations if query in station['Address'].lower()] 
    return render_template('search_results.html', results=results)
    
