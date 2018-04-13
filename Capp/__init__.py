from flask import (Flask, render_template,Response,
                    request, session, redirect, url_for, abort)
from flask_login import (LoginManager, UserMixin,
                            login_required, login_user, logout_user,
                            current_user)

from flask_socketio import SocketIO, emit, join_room, leave_room

from werkzeug.security import generate_password_hash, \
     check_password_hash

from flask_bcrypt import Bcrypt

from .models import *

from flask_migrate import Migrate

from flask_session import Session

from collections import defaultdict

from  more_itertools import unique_everseen

from sqlalchemy import and_ , or_

import json

app = Flask(__name__)
# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/Capp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"] = 'filesystem'
app.config['TESTING'] = False
Session(app)
expire_on_commit = False

app.config['SECRET_KEY'] = 'secret_key'
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
socketio = SocketIO(app=app)

# hier worden alle gespreken tijdeijk in op geslagen
message_list = defaultdict(list)

# bij houden wie  met elkaar in de kamer zitten

room_list = defaultdict(list)

# lijst van end note van specefieke gebruikers
clients_ids = defaultdict(list)

# opject van de friend list
friend_object = defaultdict(list)


import Capp.chat
import Capp.views
import Capp.dbEvent







#if __name__ == "__main__":
    #app.run(debug=True, use_reloader=True, host='0.0.0.0',threaded=True)
