from flask import Flask

from flask_bcrypt import Bcrypt



from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:1234@localhost:5432/Capp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config.from_pyfile('flask.cfg')
db.init_app(app)
bcrypt = Bcrypt(app)

def main():

    db.drop_all()
    db.create_all()
    print('dsadas')
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        main()
