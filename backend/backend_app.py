from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 2, "title": "Second post", "content": "AThis is the second post."}
]


@app.errorhandler(404)
def not_found_error(error):
    """Handles 404 Not Found errors."""
    return jsonify({"error": "Not Found"}), 404


def validate_blog_data(blog):
    """
    Validates the blog data.

    Args:
        blog (dict): The blog data.

    Returns:
        bool: True if the blog data is valid, False otherwise.
    """
    if "title" not in blog or "content" not in blog:
        return False
    return True


def find_blog(blog_id):
    """
    Finds a blog by its ID.

    Args:
        blog_id (int): The ID of the blog.

    Returns:
        dict: The blog with the specified ID, or None if not found.
    """
    blog = [blog for blog in POSTS if blog['id'] == blog_id]
    if blog == []:
        return None
    else:
        return blog[0]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """
    Handles GET and POST requests for the '/api/posts' route.

    Returns:
        flask.Response: The response containing the blog posts.
    """
    if request.args.to_dict() != {}:
        sort = request.args.get('sort')
        direction = request.args.get('direction')

        try:
            sorted_list = POSTS
            if direction == 'asc':
                sorted_list = sorted(sorted_list, key=lambda x: x[sort])
            elif direction == 'desc':
                sorted_list = sorted(sorted_list, key=lambda x: x[sort], reverse=True)
        except KeyError:
            return f"400 BAD REQUEST: Invalid 'sort' or 'direction' parameters.", 400

        return jsonify(sorted_list)

    if request.method == 'POST':
        new_blog_post = request.get_json()

        if not validate_blog_data(new_blog_post):
            return jsonify({"error": "Invalid blog data. Missing either title or content."}), 400

        new_blog_post['id'] = POSTS[-1]['id'] + 1
        POSTS.append(new_blog_post)
        return jsonify(new_blog_post), 201

    return jsonify(POSTS)


@app.route('/api/posts/<id>', methods=['DELETE'])
def delete(id):
    """
    Handles DELETE requests for the '/api/posts/<id>' route.

    Args:
        id (str): The ID of the blog post to delete.

    Returns:
        flask.Response: The response indicating the success or failure of the deletion.
    """
    blog = find_blog(int(id))

    if blog is None:
        return "This blog couldn't be found!", 404

    blog_index = POSTS.index(blog)
    del POSTS[blog_index]

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<id>', methods=['PUT'])
def update(id):
    """
    Handles PUT requests for the '/api/posts/<id>' route.

    Args:
        id (str): The ID of the blog post to update.

    Returns:
        flask.Response: The response containing the updated blog post.
    """
    blog = find_blog(int(id))

    if blog is None:
        return "This blog couldn't be found!", 404

    new_blog = request.get_json()
    blog.update(new_blog)

    return jsonify(blog)


@app.route('/api/posts/search')
def search():
    """
    Handles GET requests for the '/api/posts/search' route.

    Returns:
        flask.Response: The response containing the search results.
    """
    title = request.args.get('title')
    content = request.args.get('content')
    search_blog = [blog for blog in POSTS if title == blog['title'] or content == blog['content']]
    if search_blog == []:
        return '[]'
    return jsonify(search_blog[0])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
