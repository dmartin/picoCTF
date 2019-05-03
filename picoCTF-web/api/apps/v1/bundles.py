"""
Bundle related endpoints.

Bundle resources are treated differently as the source of truth for most of
their properties is the shell server(s). See ./problems.py for more info.
"""
from flask import jsonify
from flask_restplus import Namespace, Resource

import api.bundles
from api.common import PicoException

from .schemas import bundle_patch_req

ns = Namespace('bundles', description='Bundle management')

# @require_admin
@ns.route('/')
class BundleList(Resource):
    """Get the full list of bundles."""

    def get(self):
        """Get the full list of bundles."""
        return api.bundles.get_all_bundles(), 200

    @ns.response(501, 'Use the /problems endpoint')
    def patch(self):
        """Not implemented: use the /problems endpoint to update bundles."""
        raise PicoException(
            'Use the /problems endpoint to update bundles.',
            status_code=501)

# @require_admin
@ns.response(200, 'Success')
@ns.response(404, 'Bundle not found')
@ns.route('/<string:bundle_id>')
class Bundle(Resource):
    """Get or update the dependencies_enabled property of a specific bundle."""

    def get(self, bundle_id):
        """Retrieve a specific bundle."""
        bundle = api.bundles.get_bundle(bundle_id)
        if not bundle:
            raise PicoException('Bundle not found', status_code=404)
        return bundle, 200

    @ns.response(400, 'Error parsing request')
    @ns.expect(bundle_patch_req)
    def patch(self, bundle_id):
        """
        Update a specific bundle.

        The only valid field for this method is "dependencies_enabled".
        Other fields are pulled from the shell server, and
        can be updated via the /problems endpoint.
        """
        req = bundle_patch_req.parse_args(strict=True)
        bid = api.bundles.set_bundle_dependencies_enabled(
            bundle_id, req['dependencies_enabled'])
        if not bid:
            raise PicoException('Bundle not found', status_code=404)
        else:
            res = jsonify({
                "success": True
            })
            res.status_code = 200
            return res