from vehicle_tracker import db


class Vehicle(db.Model):
    """
    Creates a table that holds all vehicles consisting of 1 columns.
    vehidle uuid.
    """
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_uuid = db.Column(db.String(36))


class Registration(db.Model):
    """
    Creates a table that holds info regarding vehicles registering/deregistering.
    It consists of 3 columns: vehicle id, action, and time.
    """
    __tablename__ = 'registration'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    action = db.Column(db.String(10))
    time = db.Column(db.DateTime)

    # Many to one relationship with vehicle table. Each vehicle can have be registered/deregistered.
    vehicle = db.relationship('Vehicle', backref=db.backref('registrations', lazy=True))


class Location(db.Model):
    """
    Creates a table that holds info regarding movement updates of vehicles.
    It consists of 4 columns: vehicle id, latitude, longitude, and time.
    """
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    time = db.Column(db.DateTime)

    # Many to one relationship with vehicle table. Each vehicle can have multiple locations.
    vehicle = db.relationship('Vehicle', backref=db.backref('locations', lazy=True))

    @classmethod
    def get_latest_entries(cls, since):
        qs = cls.query.filter(cls.time > since).group_by(cls.vehicle_id).all()
        return qs


db.create_all()
