from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

import models
# from resources.user_dogs import user_dogs
# from resources.users import users
# from resources.dogs import dog

app = Flask(__name__)

# need this so login_manager can do its job, has to be put before we instantiate
app.config.from_pyfile('config.py')

login_manager = LoginManager() # written in JS: loginManager = new LoginManager() - we are instantiating
login_manager.init_app(app) # taking instance of this login_manager and initializing in our app called app in line 9 above

@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get_by_id(user_id)
    except models.DoesNotExist:
        return None

# @ is a decorator - a flash built in - represents functions that are build in from our packages
# Python has a really interesting feature called function decorators. This allows some really neat things for web applications. Because each view in Flask is a function, decorators can be used to inject additional functionality to one or more functions
@app.before_request
def before_request():
    # """connect to the database before each request."""
    g.db = models.DATABASE # MAKE SURE THIS IS IN CAPS since it is how it exists in model.py
    g.db.connect()

@app.after_request
def after_request(response):
    # """close the database connection after each request."""
    g.db = models.DATABASE
    g.db.close()
    return response

# named app on line 10 to be for flask to use our app
CORS(app,\
     origins=['http://localhost:3000'],\
     supports_credentials=True)

# app.register_blueprint(cafe, url_prefix='/api/v1/cafes')
# app.register_blueprint(users, url_prefix='/api/v1/users')
# app.register_blueprint(user_cafes, url_prefix='/api/v1/user_cafes')

@app.route('/')
def index():
    return 'hey folks!'
    # python uses return to send back responses rather than res.send or res.render

@app.route('/sayhello/<name>')
def say_hello(name):

    band = request.args.get('bandname')

    return jsonify(
        msg='hello', 
        bandname=band,
        status=200, 
        list=["bob", "ricky"], 
        artist="fatima " + name)

# run app
if __name__ == '__main__':
    models.initialize()
    app.run(port=8000, debug=True)

# source .env/bin/activate
# python3 app.py (postgres should be running)