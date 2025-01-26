from app.repositories.base_repository import BaseRepository
import json
import pandas as pd


class MapRepository(BaseRepository):
    def get_geojson(self):
        with open('updated_output.geojson', 'r') as f:
            return json.load(f)
        
        
    def  get_charging_stations(self):
    # Load the charging station dataset
        df_lstat = pd.read_excel("app/datasets/Ladesaeulenregister_SEP.xlsx", header=10)
        df_postcode = pd.read_csv("app/datasets/Postcode_BerlinDistricts.csv")

        # Normalize the 'Ort' column and filter for Berlin
        df_lstat['Ort'] = df_lstat['Ort'].str.strip().str.lower()
        df_lstat = df_lstat.loc[df_lstat['Ort'] == 'berlin']

        # Extract and rename relevant columns
        charging_stations = df_lstat[['Anzeigename (Karte)', 'Straße', 'Hausnummer', 'Breitengrad', 'Längengrad', "PLZ"]]

        # Drop rows with missing latitude or longitude
        charging_stations = charging_stations.dropna(subset=['Breitengrad', 'Längengrad'])

        # Convert latitude and longitude to float
        charging_stations['Latitude'] = charging_stations['Breitengrad'].str.replace(',', '.').astype(float)
        charging_stations['Longitude'] = charging_stations['Längengrad'].str.replace(',', '.').astype(float)

        # Filter out invalid coordinates
        charging_stations = charging_stations[
            (charging_stations['Latitude'].between(-90, 90)) &
            (charging_stations['Longitude'].between(-180, 180))
        ]

        # Combine "Straße" and "Hausnummer" into a single address string
        charging_stations['Address'] = charging_stations['Straße'] + ' ' + charging_stations['Hausnummer'].astype(str)
        charging_stations['id'] = range(1, len(charging_stations) + 1)
        # Rename columns to match expected keys
        charging_stations = charging_stations.rename(columns={
            'Anzeigename (Karte)': 'Name',
            'Breitengrad': 'Latitude',
            'Längengrad': 'Longitude'
        })

        # Assign unique IDs to each station
        charging_stations['id'] = range(1, len(charging_stations) + 1)
        charging_stations['Name'] = charging_stations['Name'].fillna("No Company Listed")
        charging_stations['PLZ'] = charging_stations['PLZ'].astype(str).str.zfill(5)

        df_postcode = df_postcode.rename(columns={
        'Postcode': 'PLZ'
        })
        df_postcode['PLZ'] = df_postcode['PLZ'].astype(str).str.zfill(5)
        merged_df = charging_stations.merge(df_postcode, on='PLZ', how='inner')
        merged_df['Ort'] = merged_df['District']
        merged_df.drop('District', axis=1, inplace=True)

        # Convert to a list of dictionaries
        charging_stations = merged_df[['id', 'Name', 'Address','Ort', 'Latitude', 'Longitude', 'PLZ']].to_dict('records')

        return charging_stations


    # def get_station_by_id(self, station_id):
    #     query = '''
    #         SELECT id, Name, Address, Latitude, Longitude, PLZ
    #         FROM charging_stations
    #         WHERE id = ?
    #     '''
    #     result = self.fetchone(query, (station_id,))
    #     if result:
    #         return {
    #             "id": result[0],
    #             "Name": result[1],
    #             "Address": result[2],
    #             "Latitude": result[3],
    #             "Longitude": result[4],
    #             "PLZ": result[5]
    #         }
    #     return None
