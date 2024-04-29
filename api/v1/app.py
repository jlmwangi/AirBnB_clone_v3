#!/usr/bin/python3
"""defines and initializes flask app"""

from api.v1.views import app_views
from flask import Flask
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error=None):
    """calls the storage.close method"""
    try:
        storage.close()
    except Exception as e:
        print("{}".format(ei))


if __name__ == "__main__":
    import os
    hbnb_api_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    hbnb_api_port = int(os.getenv('HBNB_API_PORT', 5000))

    app.run(host=hbnb_api_host, port=hbnb_api_port, threaded=True)
