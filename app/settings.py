import os
import certifi


MONGODB_SETTINGS = {
    'db': 'animescope',
    'host': os.environ.get("MONGO_ANIMESCOPE"),
    'tlsCAFile': certifi.where()
}