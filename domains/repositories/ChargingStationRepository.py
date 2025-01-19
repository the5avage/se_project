import sqlite3
from datetime import datetime
from domains.entities.ChargingStation import ChargingStation

class ChargingStationRepository:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def add(self, charging_station: ChargingStation):
        with self._connect() as conn:
            cursor = conn.cursor()
            # Insert the charging station
            cursor.execute(
                """
                INSERT INTO charging_stations (street, city, state, zip_code, country, capacity)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    charging_station.address.street,
                    charging_station.address.city,
                    charging_station.address.state,
                    charging_station.address.zip_code,
                    charging_station.address.country,
                    charging_station.capacity,
                ),
            )
            station_id = cursor.lastrowid

            # Insert reviews
            for review in charging_station.reviews:
                cursor.execute(
                    """
                    INSERT INTO reviews (rating, comment, created_at, reviewer_id, charging_station_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        review.rating,
                        review.comment,
                        review.created_at.isoformat(),
                        review.reviewer_id,
                        station_id,
                    ),
                )
            conn.commit()

    def get(self, station_id: int) -> ChargingStation:
        with self._connect() as conn:
            cursor = conn.cursor()

            # Fetch the charging station
            cursor.execute(
                """
                SELECT street, city, state, zip_code, country, capacity
                FROM charging_stations
                WHERE id = ?
                """,
                (station_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            address = Address(
                street=row[0], city=row[1], state=row[2], zip_code=row[3], country=row[4]
            )
            capacity = row[5]

            # Fetch the reviews
            cursor.execute(
                """
                SELECT rating, comment, created_at, reviewer_id
                FROM reviews
                WHERE charging_station_id = ?
                """,
                (station_id,),
            )
            reviews = [
                Review(
                    rating=r[0],
                    comment=r[1],
                    created_at=datetime.fromisoformat(r[2]),
                    reviewer_id=r[3],
                )
                for r in cursor.fetchall()
            ]

            return ChargingStation(id=station_id, address=address, capacity=capacity, reviews=reviews)

    def delete(self, station_id: int):
        with self._connect() as conn:
            cursor = conn.cursor()

            # Delete reviews
            cursor.execute(
                "DELETE FROM reviews WHERE charging_station_id = ?", (station_id,)
            )

            # Delete charging station
            cursor.execute(
                "DELETE FROM charging_stations WHERE id = ?", (station_id,)
            )
            conn.commit()
