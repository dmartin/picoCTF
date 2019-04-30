"""Routing functions for /api/admin."""
from bson import json_util
from flask import Blueprint, current_app, request

import api.admin
import api.common
import api.config
import api.logger
import api.problem
import api.problem_feedback
import api.shell_servers
import api.stats
import api.user
from api.annotations import require_admin
from api.common import WebError, WebSuccess

blueprint = Blueprint("admin_api", __name__)

# (/v1/problems, although feedback is not included currently)
# check if not displaying feedback or bundles in the new
# endpoint is a frontend problem

@blueprint.route('/problems', methods=['GET'])
@require_admin
def get_problem_data_hook():
    problems = list(
        filter(lambda p: len(p["instances"]) > 0,
               api.problem.get_all_problems(show_disabled=True)))

    for problem in problems:
        problem["reviews"] = api.problem_feedback.get_problem_feedback(
            pid=problem["pid"])

    data = {"problems": problems, "bundles": api.problem.get_all_bundles()}

    return WebSuccess(data=data), 200


@blueprint.route('/users', methods=['GET'])
@require_admin
def get_all_users_hook():
    users = api.user.get_all_users()
    if users is None:
        return WebError("There was an error query users from the database.")
    return WebSuccess(data=users), 200


@blueprint.route('/exceptions', methods=['GET'])
@require_admin
def get_exceptions_hook():
    try:
        limit = abs(int(request.args.get("limit")))
        exceptions = api.admin.get_api_exceptions(result_limit=limit)
        return WebSuccess(data=exceptions)

    except (ValueError, TypeError):
        return WebError("limit is not a valid integer."), 400


@blueprint.route('/exceptions/dismiss', methods=['POST'])
@require_admin
def dismiss_exceptions_hook():
    trace = request.form.get("trace", None)
    if trace:
        api.admin.dismiss_api_exceptions(trace)
        return WebSuccess(
            data="Successfully changed exception visibility."), 200
    else:
        return WebError(message="You must supply a trace to hide."), 400


@blueprint.route("/problems/submissions", methods=["GET"])
@require_admin
def get_problem():
    submission_data = {
        p["name"]: api.stats.get_problem_submission_stats(pid=p["pid"])
        for p in api.problem.get_all_problems(show_disabled=True)
    }
    return WebSuccess(data=submission_data), 200


@blueprint.route("/problems/availability", methods=["POST"])
@require_admin
def change_problem_availability_hook():
    pid = request.form.get("pid", None)
    desired_state = request.form.get("state", None)

    if desired_state is None:
        return WebError("Problems are either enabled or disabled."), 500
    else:
        state = json_util.loads(desired_state)

    api.admin.set_problem_availability(pid, state)
    return WebSuccess(data="Problem state changed successfully."), 200

# done (v1/shell_servers)
@blueprint.route("/shell_servers", methods=["GET"])
@require_admin
def get_shell_servers():
    return WebSuccess(data=api.shell_servers
                              .get_all_servers()), 200

# done
@blueprint.route("/shell_servers/add", methods=["POST"])
@require_admin
def add_shell_server():
    params = api.common.flat_multi(request.form)
    api.shell_servers.add_server(params)
    return WebSuccess("Shell server added."), 201

# done
@blueprint.route("/shell_servers/update", methods=["POST"])
@require_admin
def update_shell_server():
    params = api.common.flat_multi(request.form)

    sid = params.get("sid", None)
    if sid is None:
        return WebError("Must specify sid to be updated"), 400

    api.shell_servers.update_server(sid, params)
    return WebSuccess("Shell server updated."), 200

# done
@blueprint.route("/shell_servers/remove", methods=["POST"])
@require_admin
def remove_shell_server():
    sid = request.form.get("sid", None)
    if sid is None:
        return WebError("Must specify sid to be removed"), 400

    api.shell_servers.remove_server(sid)
    return WebSuccess("Shell server removed."), 200

# done (PATCH v1/problems)
@blueprint.route("/shell_servers/load_problems", methods=["POST"])
@require_admin
def load_problems_from_shell_server():
    sid = request.form.get("sid", None)

    if sid is None:
        return WebError("Must provide sid to load from."), 400

    number = api.shell_servers.load_problems_from_server(sid)
    return WebSuccess(
        "Loaded {} problems from the server".format(number)), 200


# done
@blueprint.route("/shell_servers/check_status", methods=["GET"])
@require_admin
def check_status_of_shell_server():
    sid = request.args.get("sid", None)

    if sid is None:
        return WebError("Must provide sid to load from."), 400

    all_online, data = api.shell_servers.get_problem_status_from_server(sid)

    if all_online:
        return WebSuccess("All problems are online", data=data), 200
    else:
        return WebError(
            "One or more problems are offline. " +
            "Please connect and fix the errors.",
            data=data), 200


@blueprint.route("/shell_servers/reassign_teams", methods=['POST'])
@require_admin
def reassign_teams_hook():
    if not api.config.get_settings()["shell_servers"]["enable_sharding"]:
        return WebError(
            "Enable sharding first before assigning server numbers."), 500
    else:
        include_assigned = request.form.get("include_assigned", False)
        count = api.shell_servers.reassign_teams(
            include_assigned=include_assigned)
        if include_assigned:
            action = "reassigned."
        else:
            action = "assigned."
        return WebSuccess(str(count) + " teams " + action), 200


@blueprint.route("/bundle/dependencies_active", methods=["POST"])
@require_admin
def bundle_dependencies():
    bid = request.form.get("bid", None)
    state = request.form.get("state", None)

    if bid is None:
        return WebError("Must provide bid to load from."), 400

    if state is None:
        return WebError("Must provide a state to set."), 400

    state = json_util.loads(state)

    api.problem.set_bundle_dependencies_enabled(bid, state)

    return WebSuccess(
        "Dependencies are now {}."
        .format("enabled" if state else "disabled")), 200


@blueprint.route("/settings", methods=["GET"])
@require_admin
def get_settings():
    return WebSuccess(data=api.config.get_settings()), 200


@blueprint.route("/settings/change", methods=["POST"])
@require_admin
def change_settings():
    data = json_util.loads(request.form["json"])
    api.config.change_settings(data)
    # May need to recreate the Flask-Mail object if mail settings changed
    api.update_mail_config(current_app)
    api.logger.setup_logs({"verbose": 2})
    return WebSuccess("Settings updated"), 200