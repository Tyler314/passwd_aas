from flask import Flask
from flask import request
from flask import abort
import json
import passwd

app = Flask("passwd_aas")
GET = passwd.Get()


@app.route("/users")
def users():
    """Returns a JSON of all users on the system.
    """
    out = GET.users()
    if not out:
        abort(404)
    return json.dumps(out)


@app.route("/users/query")
def users_query():
    """Returns a list of users matching all of the specified query fields.
    """
    try:
        name = request.args.get("name")
        uid = int(request.args.get("uid")) if request.args.get("uid") is not None else None
        gid = int(request.args.get("gid")) if request.args.get("gid") is not None else None
        comment = request.args.get("comment")
        home = request.args.get("home")
        shell = request.args.get("shell")
        out = GET.users(name, uid, gid, comment, home, shell)
        if not out:
            abort(404)
        return json.dumps(out)
    except ValueError:
        abort(404)


@app.route("/users/<int:uid>")
def users_uid(uid):
    """Return a single user with specified uid. Return 404 if the uid is not found.
    """
    out = GET.users(uid=uid)
    if not out:
        abort(404)
    return json.dumps(out.pop())


@app.route("/users/<int:uid>/groups")
def groups_of_user(uid):
    """Return all the groups for a given user.
    """
    out = GET.groups_by_uid(uid)
    if not out:
        abort(404)
    return json.dumps(out)


@app.route("/groups")
def groups():
    """Return a list of all groups on the system, a defined by the group file.
    """
    out = GET.groups()
    if not out:
        abort(404)
    return json.dumps(out)


@app.route("/groups/query")
def groups_query():
    """Returns a list of groups matching all of the specified query fields.
    """
    try:
        name = request.args.get("name")
        gid = int(request.args.get("gid")) if request.args.get("gid") is not None else None
        members = request.args.getlist("member")
        out = GET.groups(name, gid, members)
        if not out:
            abort(404)
        return json.dumps(out)
    except ValueError:
        abort(404)


@app.route("/groups/<int:gid>")
def groups_uid(gid):
    """Return a single group with the gid. Return 404 if the gid is not found
    """
    out = GET.groups(gid=gid)
    if not out:
        abort(404)
    return json.dumps(out.pop())


def run_app(passwd_path, group_path, port):
    """Entry point for the application
    """
    GET.set_passwd_path(passwd_path)
    GET.set_group_path(group_path)
    app.run(port=port)
