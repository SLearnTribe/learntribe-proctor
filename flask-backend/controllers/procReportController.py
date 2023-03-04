import json

from flask_classful import FlaskView, route
from flask import jsonify, request

from authorization.jwtVerifier import jwt_verification


class ProcReportController(FlaskView):

    def index(self):
        return jsonify(message="Invalid api, bad request"), 400

    @route('/report', methods=['PUT'])
    @jwt_verification
    def insert(self):
        data = {'userID': request.args.get('userId'),
                'assessmentId': request.args.}

    # @route('/db_create', methods=['GET'])
    # @jwt_verification
    # def (self, keycloak_id):  # For Development
    #     if keycloak_id is None:
    #         return jsonify(message="Keycloak_id can't be empty"), 402
    #     result = self.analytics_service.retrieve_candidate_activities(keycloak_id=keycloak_id)
    #
    #     return result, 202
