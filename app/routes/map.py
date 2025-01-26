from flask import Blueprint, render_template
from app.domains.events.map_events import handle_home_event, handle_station_info_event, handle_contact_event

map_bp = Blueprint("map", __name__)

@map_bp.route('/')
def home():
    return handle_home_event()

@map_bp.route('/station_info/<int:station_id>', methods=['GET'])
def station_info(station_id):
    return handle_station_info_event(station_id)

@map_bp.route('/contact', methods=['GET'])
def contact():
    return handle_contact_event()
