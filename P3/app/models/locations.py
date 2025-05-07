from app.utils.database import get_db


class Location:
    def __init__(self, id, address, city, state, zip_code):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    @staticmethod
    def create(address, city, state, zip_code):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO locations (address, city, state, zip_code)
               VALUES (?, ?, ?, ?)""",
            (address, city, state, zip_code),
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def get(location_id):
        db = get_db()
        location = db.execute("""SELECT * FROM locations WHERE id = ?""", (location_id,)).fetchone()

        if location is None:
            return None

        return Location(
            id=location["id"],
            address=location["address"],
            city=location["city"],
            state=location["state"],
            zip_code=location["zip_code"],
        )

    @staticmethod
    def get_all():
        db = get_db()
        locations = db.execute("""SELECT * FROM locations ORDER BY city, state""").fetchall()
        return locations

    def update(self):
        db = get_db()
        db.execute(
            """UPDATE locations
               SET address = ?,
                   city = ?,
                   state = ?,
                   zip_code = ?
               WHERE id = ?""",
            (self.address, self.city, self.state, self.zip_code, self.id),
        )
        db.commit()

    def delete(self):
        db = get_db()
        db.execute("DELETE FROM locations WHERE id = ?", (self.id,))
        db.commit()

    @staticmethod
    def search(query):
        db = get_db()
        search_term = f"%{query}%"
        locations = db.execute(
            """SELECT * FROM locations 
               WHERE address LIKE ? 
               OR city LIKE ? 
               OR state LIKE ?
               OR zip_code LIKE ?""",
            (search_term, search_term, search_term, search_term),
        ).fetchall()
        return locations

    def get_google_maps_embed_url(self):
        """Generate a Google Maps embed URL for the location."""
        query = f"{self.address}, {self.city}, {self.state}, {self.zip_code}"
        return f"https://www.google.com/maps/embed/v1/place?key=YOUR_GOOGLE_MAPS_API_KEY&q={query.replace(' ', '+')}"
