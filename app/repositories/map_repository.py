from app.repositories.base_repository import BaseRepository
import json

class MapRepository(BaseRepository):
    def get_geojson(self):
        with open('updated_output.geojson', 'r') as f:
            return json.load(f)

    def get_charging_stations(self):
        query = '''
            SELECT id, Name, Address, Latitude, Longitude, PLZ
            FROM charging_stations
        '''
        results = self.fetchall(query)
        return [
            {
                "id": row[0],
                "Name": row[1],
                "Address": row[2],
                "Latitude": row[3],
                "Longitude": row[4],
                "PLZ": row[5]
            }
            for row in results
        ]

    def get_station_by_id(self, station_id):
        query = '''
            SELECT id, Name, Address, Latitude, Longitude, PLZ
            FROM charging_stations
            WHERE id = ?
        '''
        result = self.fetchone(query, (station_id,))
        if result:
            return {
                "id": result[0],
                "Name": result[1],
                "Address": result[2],
                "Latitude": result[3],
                "Longitude": result[4],
                "PLZ": result[5]
            }
        return None
