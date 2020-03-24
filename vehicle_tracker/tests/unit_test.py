import json
import uuid
from datetime import datetime, timedelta
from unittest import mock
import pytest
from vehicle_tracker import app, model


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def vehicle_id():
    """
    Generates a random uuid that represents a vehicle id
    :return:
    """
    return str(uuid.uuid1())


def register_vehicle(client, vehicle_id):
    """
    Registers a vehicle by sending a POST request to our client that consists of
    the vehicle it
    :param client:
    :param vehicle_id:
    :return:
    """
    return client.post('/vehicles', data=json.dumps({'id': vehicle_id}), content_type='application/json')


def update_location(client, vehicle_id, lat, lng):
    """
    Updates location of a vehicle by sending a POST request to our client
    that consists of the vehicle id, latitude and longitude and time
    :param client:
    :param vehicle_id:
    :param lat:
    :param lng:
    :return:
    """
    now = datetime.isoformat(datetime.utcnow())
    return client.post('/vehicles/%s/locations' % vehicle_id,
                       data=json.dumps({'lat': lat,
                                        'lng': lng,
                                        'at': now}),
                       content_type='application/json')


def test_register_vehicle(client, vehicle_id):
    """
    Testing registering vehicle successfully
    :param client:
    :param vehicle_id:
    :return:
    """
    res = register_vehicle(client, vehicle_id)
    vehicle = model.Vehicle.query.filter_by(vehicle_uuid=vehicle_id).first()

    # Assert that the vehicle id is correct, action is register, return code is 204 and body is empty
    assert vehicle.vehicle_uuid == vehicle_id
    assert vehicle.registrations[-1].action == 'register'
    assert res.status_code == 204
    assert res.data == b''


@mock.patch('flask_socketio.SocketIO.emit')
def test_update_location(socketio, client, vehicle_id):
    """
    Testing updating location of vehicle
    :param socketio:
    :param client:
    :param vehicle_id:
    :return:
    """
    register_vehicle(client, vehicle_id)
    res = update_location(client, vehicle_id, 52.53, 13.403)
    since = datetime.utcnow() - timedelta(seconds=2)
    entry = model.Location.get_latest_entries(since)[-1]
    expected = mock.call('update_location',
                         {'vehicle_id': vehicle_id,
                          'lat': 52.53, 'lng': 13.403},
                         namespace='/vehicles')
    # Check if the websocket is reached successfully
    assert socketio.called
    assert socketio.call_args == expected

    # Assert that the vehicle id is correct, correct location, return code is 204 and body is empty
    assert entry.vehicle.vehicle_uuid == vehicle_id
    assert entry.lat, entry.lgn == (52.53, 13.403)
    assert res.status_code == 204
    assert res.data == b''


@mock.patch('flask_socketio.SocketIO.emit')
def test_update_location_out_of_boundaries(socketio, client, vehicle_id):
    """
    Testing updating location of vehicle that goes our of city boundaries
    :param socketio:
    :param client:
    :param vehicle_id:
    :return:
    """
    register_vehicle(client, vehicle_id)
    res = update_location(client, vehicle_id, 51.2, 45.3)
    expected = mock.call('deregister_vehicle',
                         {'vehicle_id': vehicle_id},
                         namespace='/vehicles')

    # Check if the websocket is reached successfully
    assert socketio.called
    assert socketio.call_args == expected

    # Assert that return code is 204 and body is empty
    assert res.status_code == 204
    assert res.data == b''


@mock.patch('flask_socketio.SocketIO.emit')
def test_deregister_vehicle(socketio, client, vehicle_id):
    """
    Testing deregistering vehicle
    :param socketio:
    :param client:
    :param vehicle_id:
    :return:
    """
    register_vehicle(client, vehicle_id)
    res = client.delete('/vehicles/%s' % vehicle_id)
    vehicle = model.Vehicle.query.filter_by(vehicle_uuid=vehicle_id).first()
    expected = mock.call('deregister_vehicle',
                         {'vehicle_id': vehicle_id},
                         namespace='/vehicles')

    # Check if the websocket is reached successfully
    assert socketio.called
    assert socketio.call_args == expected

    # Assert that action is deregister, return code is 204 and body is empty
    assert vehicle.registrations[-1].action == 'deregister'
    assert res.status_code == 204
    assert res.data == b''
