import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

users = Blueprint("users", "users")

# register route
@users.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'].lower()

    try:
        # does the user already exit / is the username taken?
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={}, status={"code": 401,\
                                        "message": "a user with that email already exists."})

    except models.DoesNotExist:
        # if the user does not already exist ... create a user
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)

        user_dict = model_to_dict(user)

        del user_dict['password'] # don't expose password

        return jsonify(data=user_dict, status={"code": 201, "message": "successfully registered"})

# login route -- log in with email and password (not username)
@users.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    payload['email'].lower()
    
    try:
        # see if user is registered
        user = models.User.get(models.User.email == payload['email'])
        print("!!!!!!!!!!")
        print(user)

        user_dict = model_to_dict(user)

        # check_password_hash(hashed_pw_from_db, unhashed_pw_from_payload)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password'] # for security reasons, deleted hashed pw
            login_user(user) # user pulled from earlier, start session
            return jsonify(data=user_dict, status={"code": 200, "message": "success"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"})

# logout rouote
@users.route('/logout', methods=["GET", "POST"])
def logout():
    if current_user:
        logout_user()
        return jsonify(data={}, status={"code": 200, "message": "successful logout"})
    else:
        return jsonify(data={}, status={"code": 401, "message": "you are not logged in"})