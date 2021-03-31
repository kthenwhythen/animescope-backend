import os
import certifi

print("#################################")
print(os.environ.get("MONGO_ANIMESCOPE"))
print("#################################")

MONGODB_SETTINGS = {
    'db': 'animescope',
    'host': os.environ.get("MONGO_ANIMESCOPE"),
    'tlsCAFile': certifi.where()
}