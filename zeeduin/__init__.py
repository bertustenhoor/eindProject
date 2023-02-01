from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'myveryveryverysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Hanze12345@localhost/zeeenduin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from zeeduin.backend.views import backend_blueprint
from zeeduin.frontend.views import frontend_blueprint

app.register_blueprint(backend_blueprint, url_prefix='/backends')
app.register_blueprint(frontend_blueprint, url_prefix='/frontends')
