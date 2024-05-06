from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Cross-Origin Resource Sharing. CORS is a mechanism that allows or restricts resources on a web server to be requested from another domain outside the server's domain.

# This is dummy data for demonstration. In a real system, this data would be stored in a DataBase.
users_data = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

blog_posts_data = [
    {"id": 1, "title": "Hello World", "content": "This is the first post."},
    {"id": 2, "title": "Second Post", "content": "This is another post."}
]


@app.route('/users', methods=['GET', 'POST']) # /users - this is called "endpoint". It accepts methods GET and POST - to get a list of all users and to add a new user
def users():
    if request.method == 'GET':
        return jsonify(users_data) # In a real system, this would be replaced with a DB request, such as SELECT * FROM users. By default, Flask will return HTTP code "200 OK"
    elif request.method == 'POST':
        new_user = request.json
        users_data.append(new_user) # NB: We just add incoming data to the list, and it does not have an ID in it. Try adding the ID of a user here. 
        return jsonify(new_user), 201 # 201 - HTTP CODE that means "Created" - it tells the frontend that a new entry has been created.

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE']) # This function deals with a single user, identifyed by a user_id, which is passed to the function as an argument
def user(user_id):
    user = next((u for u in users_data if u["id"] == user_id), None)  # First, we a searching for a user with give ID
    if user is None:
        return jsonify({"error": "User not found"}), 404 # If the user is not found in our DataBase, return code 404 - Not Found. Meaning, the frontend requested smth that does not exist.

    if request.method == 'GET':
        return jsonify(user)
    elif request.method == 'PUT':
        updated_data = request.json 
        user.update(updated_data) # Here, we are just updating a Python Dictionary, meaning, we can either add or modify fields, but not remove them.
        return jsonify(user) # By default, the return code will "200 OK" - we don't need to specify it here, only return the data.
    elif request.method == 'DELETE':
        users_data.remove(user)
        return '', 204 # Returning code 204 - No Content - Unlike 404 this code means that the request was successful, but there is nothign to return (we return empty string). 

@app.route('/blog_posts', methods=['GET', 'POST'])
def blog_posts():
    if request.method == 'GET':
        return jsonify(blog_posts_data)
    elif request.method == 'POST':
        new_post = request.json
        blog_posts_data.append(new_post)
        return jsonify(new_post), 201

@app.route('/blog_posts/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
def blog_post(post_id):
    post = next((p for p in blog_posts_data if p["id"] == post_id), None)
    if post is None:
        return jsonify({"error": "Blog post not found"}), 404

    if request.method == 'GET':
        return jsonify(post)
    elif request.method == 'PUT':
        updated_data = request.json
        post.update(updated_data)
        return jsonify(post)
    elif request.method == 'DELETE':
        blog_posts_data.remove(post)
        return '', 204


if __name__ == "__main__":
    app.run()
