import uuid
from datetime import datetime
from dateutil.parser import parse as parse_iso
from flask import render_template, request
from haversine import haversine
from vehicle_tracker import app, db, model, socketio


@app.route('/')
def index():
    return render_template('index.html', mapbox_key=app.config['MAPBOX_KEY'])


@app.route('/vehicles', methods=['POST'])
def register_vehicle():
    """
    Registers new vehicle by uuid if it doesn't already exist in our database.
    :return:
    """

    try:
        vehicle_id = str(uuid.UUID(request.get_json()['id']))
    except KeyError:
        return 'Vehicle uuid was NOT provided', 400
    except ValueError:
        return 'Vehicle uuid is NOT valid', 400

    vehicle = model.Vehicle.query.filter_by(vehicle_uuid=vehicle_id).first()
    if not vehicle:
        vehicle = model.Vehicle(vehicle_uuid=vehicle_id)
        db.session.add(vehicle)

    model.Registration(vehicle=vehicle,
                       action='register',
                       time=datetime.utcnow())
    db.session.commit()

    return '', 204


@app.route('/vehicles/<uuid:vehicle_id>', methods=['DELETE'])
def deregister_vehicle(vehicle_id):
    """
    Deregister vehicle with given vehicle id.
    :param vehicle_id:
    :return:
    """

    vehicle_id = str(vehicle_id)
    vehicle = model.Vehicle.query.filter_by(vehicle_uuid=vehicle_id).first()
    if not vehicle:
        return 'Vehicle does NOT exist', 404

    # Deregister vehicle and persist
    model.Registration(vehicle=vehicle,
                       action='deregister',
                       time=datetime.utcnow())
    db.session.commit()

    # Send to the socket check if vehicle is within allowed city boundaries
    socketio.emit('deregister_vehicle',
                  {'vehicle_id': str(vehicle_id)},
                  namespace='/vehicles')

    return '', 204


@app.route('/vehicles/<uuid:vehicle_id>/locations', methods=['POST'])
def update_location(vehicle_id):
    """
    Updates a vehicle with current location bases on it's uuid.
    :param vehicle_id:
    :return:
    """

    vehicle_id = str(vehicle_id)
    vehicle = model.Vehicle.query.filter_by(vehicle_uuid=vehicle_id).first()
    if not vehicle:
        return 'Vehicle does NOT exist', 404

    if vehicle.registrations[-1].action != 'register':
        return 'Vehicle is NOT registered', 401

    data = request.get_json()

    # Only allow to update vehicle's current location if lat and lng is
    # within city boundaries
    if haversine((data['lat'], data['lng']), (52.53, 13.403)) <= 3.5:
        model.Location(vehicle=vehicle,
                       lat=data['lat'],
                       lng=data['lng'],
                       time=parse_iso(data['at']))
        db.session.commit()

        # Send to the socket to visually update the location of the vehicle on the map
        socketio.emit('update_location',
                      {'vehicle_id': str(vehicle_id),
                       'lat': data['lat'],
                       'lng': data['lng']},
                      namespace='/vehicles')

    # Send to the socket check if vehicle is within allowed city boundaries
    else:
        socketio.emit('deregister_vehicle',
                      {'vehicle_id': str(vehicle_id)},
                      namespace='/vehicles')

    return '', 204
