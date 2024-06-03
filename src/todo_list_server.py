"""
Script to represent todo lists and todo entries in Python
data structures and to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id]), 200
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200
    return 'Server error', 500


# define endpoint for adding a new list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    if not new_list:
        abort(406)
    elif request.method == 'POST':
        print('Got new list to be added: {}'.format(new_list))
        # create id for new list, save it and return the list
        new_list['id'] = str(uuid.uuid4())
        todo_lists.append(new_list)
        return jsonify(new_list), 201
    return 'Server error', 500

# define endpoint to add a new entry to existing list
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    # make JSON from POST data (even if content type is not set correctly)
    new_entry = request.get_json(force=True)
    # if no json is invalid, return status code 406
    if not new_entry:
        abort(406)
    elif request.method == 'POST':
        print('Got new entry to be added to list: {}'.format(new_entry))
        # create id for new entry, save it and return the entry
        new_entry['id'] = str(uuid.uuid4())
        new_entry['list'] = list_id
        todos.append(new_entry)
        return jsonify(new_entry), 201
    return 'Server error', 500

# define endpoint to update entry in list
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PATCH','DELETE'])
def handle_entry(list_id, entry_id):
    entry_item = None
    # find entry for entry id
    for entry in todos:
        if entry['id'] == entry_id:    
            if entry['list'] == list_id:
                entry_item = entry
                break
    # if list id is invalid, return 404
    if not list_id:
        abort(404)
    # if entry id is invalid, return 405
    if not entry_id:
        abort(405)
    # if json is invalid, return 406
    if not entry_item:
        abort(406)
    if request.method == 'PATCH':
        # update entry
        update_entry = request.get_json(force=True)
        update_entry['id'] = entry_item['id']
        update_entry['list'] = entry_item['list']
        todos.remove(entry_item)
        todos.append(update_entry)
        return jsonify(update_entry), 201
    elif request.method == 'DELETE':
        # delete entry
        todos.remove(entry_item)
        return 'Entry changed', 200
    return 'Server error', 500

# define endpoint for getting all lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)


if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
