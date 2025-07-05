# class Config:
#     SECRET_KEY = '79da288f9993304133b20b3d2bffaa03c59055605dbf3ac9383e1fb0a151a245'
#     MONGO_URI = 'mongodb://localhost:27017/asksphere'

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/asksphere_ai')
    SECRET_KEY = os.getenv('SECRET_KEY', 'b96aaa7e5d3e3a962ac0e58ae86d7c0779413b53745b636a18ce23ed2eb6ae1f')
