import models

from flask import Blueprint, jsonify, request 
from playhouse.shortcuts import model_to_dict
from flask_login import current_user

user_cafes = Blueprint("user_cafes", "user_cafes")

# copied this from dogs.py and commented out the create_dog route in dogs.py
@user_cafes.route('/', methods=["POST"])
def create_cafe():
    # create the cafe w/ payload info if current_user exists 
    # can these be hidden forms included when a user adds a cafe to their favorites, it pulls it directly from the Cafe?
    if current_user.id:
        payload = request.get_json()
        print(payload)
        cafe = models.Cafe.create(**payload)
        cafe_dict = model_to_dict(cafe)

        # when we run this block of code, it will stop where breakpoint function and in our terminal, we wll be in python shell that allows us to view all variables in our python code.
        # breakpoint()

        # python 2 debugger:
        # import pdb (which is python debugger)
        # pdb.set_trace()
        # python 3 is breakpoint()

        # create the relationship between cafe and user
        user_cafe_data = {
            "user": current_user.id,
            "cafe": cafe.id
        }
        models.UserCafe.create(**user_cafe_data)
        return jsonify(data=cafe_dict, status={"code": 201, "message": "Success"})