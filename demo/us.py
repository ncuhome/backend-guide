from flask import Flask, request, abort


app = Flask(__name__)


@app.route("/api")
def api():
    with app.open_resource("us-api.json") as f:
        content = f.read()
    return content, 200, {"Content-Type": "application/json"}


@app.route("/api/user")
def user():
    if request.method == 'GET':
        return "user.get"
    elif request.method == 'POST':
        return "user.post"
    elif request.method == 'Delete':
        return "user.delete"
    elif request.method == 'PUT':
        return "user.put"
    elif request.method == 'POST':
        return "user.post"
    else:
        abort(404, "Not Impl")


@app.route("/api/user/me")
def user_me():
    if request.method == 'GET':
        return "user.get_me"
    else:
        abort(404, "Not Impl")

if __name__ == '__main__':
    app.run(debug=True)
