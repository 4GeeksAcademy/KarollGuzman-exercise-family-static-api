"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET', 'POST'])
def members():
    response_body = {}
    if request.method == 'GET':
       members = jackson_family.get_all_members()
       response_body['message'] = "Listado de los integrantes de la familia"
       response_body["results"] = members
       return response_body, 200
    if request.method == 'POST':
        data = request.json
        jackson_family.add_member(data)
        response_body['results'] = jackson_family.get_all_members()
        response_body['message'] = 'Respuesta desde el POST de /members'
        return response_body, 200


@app.route('/member/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def member(id): 
    response_body = {}
    if not jackson_family.get_member(id):
        response_body['message'] = f'El miembro no existe{id}'
        response_body['results'] = []
    if request.method == 'GET':
        response_body['message'] = 'respuesta desde el GET para el usuario {id}'
        response_body['results'] = jackson_family.get_member(id)
        return response_body, 200
    if request.method == 'PUT':
        response_body['message'] = 'respuesta desde el GET para el usuario {id}'
        return response_body, 200
    if request.method == 'DELETE':
        response_body['results'] = jackson_family.delete_member(id) 
        response_body['message'] = 'respuesta desde el GET para el usuario {id}'
        return response_body, 200

    response_body['message'] = 'respuesta desde el GET para el usuario {id}'
    return response_body, 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)