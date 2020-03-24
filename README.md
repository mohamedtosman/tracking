# Mohamed Osman

## Technologies

### Python3/Flask

I used the technologies above as Flask is super lightweight. It allows for
quick creation of webservices and is super minimalistic.

### SQLAlchemy/SQLite

I used the technologies above as SQLite is an opensource SQL database that stores data to a text file on a device.
A huge advantage of that is that it offers great accessibility and provided
Python libraries are simple to use.

### Leaflet

Leaflet is the leading open-source JavaScript library for mobile-friendly interactive maps.
After a bit of research, i found multiple tutorials explaining how it works
and it seemed easy to use and matches my needs for this project.

### Mapbox

An open source custom designed SDK for online maps.

### HTML/JavaScript/CSS
### Pytest

## Installation

1. Download this repo

2. Update `config.cfg` with your own api key for Map Box but you can use mine :)

3. Install the dependencies needed for the project defined in `setup.py`. From the root directory execute:

`pip install .`

4. Set the environment variable needed to start the Flask server:

`export FLASK_APP=vehicle_tracker`

5. Run the application from the root directory:

`flask run`

6. You can now access the application at `localhost:5000`

## Visualization

I used Mapbox and Leaflet as suggested by you guys as it seemed 
pretty straightforward and easy to use.

## API

### Register vehicle - `POST`

`/vehicles`

Path variables - N/A

Body - `{ "id": "vehicle-uuid" }`

Return code - `204`

### Deregister vehicle - `DELETE`

`/vehicles/<uuid:vehicle_id>`

Path variables - `uuid`

Body - N/A

Return code - `204`

### Update location - `POST`

`/vehicles/<uuid:vehicle_id>/locations`

Path variables - `uuid`

Body - `{ "lat": 10.0, "lng": 20.0, "at": "2020-03-24T12:00:00Z" }`

Return code - `203`

## Error Codes

`400` - Vehicle uuid was not provided/valid

`404` - Vehicle does NOT exist

`401` - Vehicle is not registered

## Database Models

### vehicle Table

Cresates a table that keeps a record of all vehicles. It consists of
1 column: `vehicle_uuid`

### registration Table

Creates a table that holds info regarding vehicles registering/deregistering.
It consists of 3 columns: `vehicle_id`, `action`, and `time`.

### location Table 

Creates a table that holds info regarding movement updates of vehicles.
It consists of 4 columns: `vehicle_id`, `lat`, `lng`, and `time`.

## Tests

I included 4 unit tests that tests the api: registering a vehicle, deregistering
a vehicle, updating vehicle's location, and updating vehicle's location
outside city boundaries.

From root directory, execute the following to run the tests:

`python -m pytest`
