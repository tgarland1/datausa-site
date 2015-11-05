# -*- coding: utf-8 -*-
from flask import abort, Blueprint, g, jsonify, render_template, request, Response
from config import PROFILES
from datausa.profile.profile import Profile
from datausa.utils.data import stat as stat_logic
from datausa import app
from flask import stream_with_context

# create the profile Blueprint
mod = Blueprint("profile", __name__, url_prefix="/profile")

@mod.before_request
def before_request():
    g.page_type = "profile"


def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(2)
    return rv

# create a route and function for the education profile that accepts a CIP id
@mod.route("/<attr_type>/<attr_id>/")
def profile(attr_type, attr_id):

    if not attr_type in PROFILES:
        abort(404);

    # pass id and type to Profile class
    p = Profile(attr_id, attr_type)
    sections = p.sections()
    # render the profile template and pass the profile to jinja_env
    return Response(stream_with_context(stream_template("profile/index.html", profile = p, sections=sections)))

@mod.route("/stat/")
def stat():
    args = {k: v for k, v in request.args.iteritems()}
    col = args.pop("col", "name")
    dataset = args.pop("dataset", False)
    if dataset == "False":
        dataset = False
    return jsonify(stat_logic(args, col=col, dataset=dataset))
