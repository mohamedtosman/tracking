from setuptools import find_packages, setup

setup(
    name='vehicle_tracker',
    version='1.0',
    license='MIT',
    description='Live vehicle tracker map',
    author='Mohamed Osman',
    author_email='mohamedtosman@cmail.carleton.ca',
    url='https://github.com/mohamedtosman/tracking',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-socketio',
        'flask-sqlalchemy',
        'python-dateutil',
        'haversine',
        'gevent',
        'gevent-websocket'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)