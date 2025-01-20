import unittest
from domains.entities.ChargingStation import ChargingStation

class TestChargingStation(unittest.TestCase):
    def test_charging_station_creation(self):
        data = {
            "Betreiber": "Berliner Stadtwerke KommunalPartner GmbH",
            "Name": "Berliner Stadtwerke KommunalPartner GmbH",
            "Straße": "Leipziger Platz",
            "Hausnummer": "19",
            "Adresszusatz": None,
            "PLZ": 1011,
            "Ort": "berlin",
            "Kreis/kreisfreie Stadt": "Kreisfreie Stadt Berlin",
            "Bundesland": "Berlin",
            "Latitude": 52.510055,
            "Longitude": 13.377592,
            "Inbetriebnahmedatum": 1688083200000,
            "Nennleistung Ladeeinrichtung [kW]": 30.0,
            "Art der Ladeeinrichtung": "Normalladeeinrichtung",
            "Anzahl Ladepunkte": 2,
            "Steckertypen1": "AC Typ 2 Steckdose",
            "P1 [kW]": 22.0,
            "Public Key1": None,
            "Steckertypen2": "AC Typ 2 Steckdose",
            "P2 [kW]": 22.0,
            "Public Key2": None,
            "Steckertypen3": None,
            "P3 [kW]": None,
            "Public Key3": None,
            "Steckertypen4": None,
            "P4 [kW]": None,
            "Public Key4": None,
            "Steckertypen5": None,
            "P5 [kW]": None,
            "Public Key5": None,
            "Steckertypen6": None,
            "P6 [kW]": None,
            "Public Key6": None,
            "Address": "Leipziger Platz 19",
            "id": 1
        }
        station = ChargingStation(data)
        self.assertEqual(station.betreiber, "Berliner Stadtwerke KommunalPartner GmbH")
        self.assertEqual(station.name, "Berliner Stadtwerke KommunalPartner GmbH")
        self.assertEqual(station.strasse, "Leipziger Platz")
        self.assertEqual(station.hausnummer, "19")
        self.assertEqual(station.plz, 1011)
        self.assertEqual(station.ort, "berlin")
        self.assertEqual(station.latitude, 52.510055)
        self.assertEqual(station.longitude, 13.377592)
        self.assertEqual(station.nennleistung_ladeeinrichtung_kw, 30.0)
        self.assertEqual(station.art_der_ladeeinrichtung, "Normalladeeinrichtung")
        self.assertEqual(station.anzahl_ladepunkte, 2)
        self.assertEqual(station.steckertypen1, "AC Typ 2 Steckdose")
        self.assertEqual(station.p1_kw, 22.0)
        self.assertEqual(station.address, "Leipziger Platz 19")
        self.assertEqual(station.id, 1)

if __name__ == "__main__":
    unittest.main()