from flask import Flask, request, jsonify
from flask_cors import CORS
import random, string
app = Flask(__name__)
CORS(app)

users = {
   'users_list' :
   [
      {
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123',
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222',
         'name': 'Mac',
         'job': 'Professor',
      },
      {
         'id' : 'yat999',
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555',
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

@app.route('/')
def hello_world():
	return 'Hello, world!'

@app.route('/users', methods=['GET', 'POST'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
      else:
         subdict = users
      if search_job:
         sub_subdict = {'users_list' : []}
         for user in subdict['users_list']:
            if user['job'] == search_job:
               sub_subdict['users_list'].append(user)
         return sub_subdict
      return subdict
   elif request.method == 'POST':
      userToAdd = request.get_json()
      if 'id' not in userToAdd:
         userToAdd['id'] = generateRandomID()
      users['users_list'].append(userToAdd)
      resp = jsonify(userToAdd)
      resp.status_code = 201
      return resp

# generates a random ID
# obviously this is less than ideal; could generate a duplicate id, but doing
# this naively for the sake of simplicity
def generateRandomID():
   letters = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
   numbers = ''.join(random.choice(string.digits) for i in range(3))
   return letters + numbers

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
   if request.method == 'GET':
      if id :
         for user in users['users_list']:
            if user['id'] == id:
               return user
         return ({})
      return users
   elif request.method == 'DELETE':
      if id:
         for user in users['users_list']:
            if user['id'] == id:
               users['users_list'].remove(user)
               return jsonify(success=True)
         return jsonify(success=False)
      return jsonify(success=False)
