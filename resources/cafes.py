import models

from flask import Blueprint, jsonify, request 
from playhouse.shortcuts import model_to_dict 

cafe = Blueprint('cafes', 'cafe')

# this is the code to get all cafes from the Yelp API - need to build in a criteria to only pull nonprofit
@cafe.route('/', methods=["GET"])
def get_all_cafes():
    ## find the dogs and change each one to a dictionary into a new array
    try:
        # this will query the DB to get all the dogs
        all_cafes = models.Cafe.select()
        # dogs = [{'dog': model_to_dict(dog), 'human': dog.human} for dog in models.Dog.select()]
        # return jsonify(data=dogs, status={""})
        print(all_cafes)
        # parse the models into dictionaries 
        cafes_to_dict = [model_to_dict(cafe) for cafe in all_cafes]

        print(cafes_to_dict)
        return jsonify(data=cafes_to_dict, status={"code": 200, "message": "Success"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# rather than :id in react, flash uses <id>
@cafe.route('/<cafe_id>', methods=["GET"])
def get_cafe(cafe_id):
    try:
        cafe = models.Cafe.get_by_id(cafe_id)
        cafe_dict = model_to_dict(cafe)
        return jsonify(data=cafe_dict, status={"code": 200, "message": "success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401,\
                                        "message": "error getting the resources"})

# not needing to updatte the cafe details since this is pulled from Yelp API -- UNLESS this is for updating the favorites list.
# would that be on a separate user_cafes.py file?

# @cafe.route('/<cafe_id>', methods=["PUT"])
# def update_cafe(cafe_id):
#     try:
#         payload = request.get_json()
#         query = models.Cafe.update(**payload).where(models.Cafe.id==cafe_id)
#         query.execute()
#         updated_cafe = model_to_dict(models.Cafe.get_by_id(cafe_id))
#         # grabbing dog and immediately turning it into dictionary

#         return jsonify(data=updated_cafe, status={"code": 200, "message": "successfully updated"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 404,\
#                                         "message": "error getting the resources"})

# same of the notes on update -- this would only be for deleting the cafe from favorites list
@cafe.route('/<cafe_id>', methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe_to_delete = models.Cafe.get_by_id(cafe_id)
    cafe_to_delete.delete_instance()

    # another way of deleting a dog
    # query = models.Dog.delete().where(models.Dog.id==dog_id)
    # query.execute()

    return jsonify(data={}, status={"code": 200, "message": "resource successfully deleted"})