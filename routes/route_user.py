from service.getter import getApiKey
from service.user.changeEmail import changeEmail
from service.user.changePassword import changePassword
from service.user.changeUsername import changeUsername
from service.user.checkUsername import checkUsername
from service.user.editDisplayName import editDisplayName
from swaggerConfig import api
from flask_restx import reqparse, Resource
from flask import jsonify, request
from service.validators.validationFunctions import validateParameters 


user = api.namespace("user", description="User Apis")

editDisplayNameUserModel = reqparse.RequestParser()
editDisplayNameUserModel.add_argument("displayName", type=str, required=True, help="Display name of user", location="json")

checkUsernameUserModel = reqparse.RequestParser()
checkUsernameUserModel.add_argument("username", type=str, required=True, help="Username of user", location="args")

editUsernameUserModel = reqparse.RequestParser()
editUsernameUserModel.add_argument("username", type=str, required=True, help="Username of user", location="json")

editEmailUserModel = reqparse.RequestParser()
editEmailUserModel.add_argument("email", type=str, required=True, help="Email of user", location="json")

changePasswordUserModel = reqparse.RequestParser()
changePasswordUserModel.add_argument("oldPassword", type=str, required=True, help="Old password of user", location="json")
changePasswordUserModel.add_argument("newPassword", type=str, required=True, help="New password of user", location="json")


@user.route("/displayName")
class EditDisplayName(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(editDisplayNameUserModel)
    def put(self):
        reqObj = validateParameters(request.json, ["displayName"])
        apiKey = getApiKey(request)
        output = editDisplayName(apiKey, reqObj)
        return jsonify(output)


@user.route("/username")
class EditUsername(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(checkUsernameUserModel)
    def get(self):
        reqObj = validateParameters(request.args, ["username"])
        apiKey = getApiKey(request)
        output = checkUsername(apiKey, reqObj)
        return jsonify(output)

    @api.doc(responses={200: "OK"})
    @api.expect(editUsernameUserModel)
    def put(self):
        reqObj = validateParameters(request.json, ["username"])
        apiKey = getApiKey(request)
        output = changeUsername(apiKey, reqObj)
        return jsonify(output)


@user.route("/email")
class EditEmail(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(editEmailUserModel)
    def put(self):
        reqObj = validateParameters(request.json, ["email"])
        apiKey = getApiKey(request)
        output = changeEmail(apiKey, reqObj)
        return jsonify(output)


@user.route("/password")
class EditPassword(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(changePasswordUserModel)
    def put(self):
        reqObj = validateParameters(request.json, ["oldPassword", "newPassword"])
        apiKey = getApiKey(request)
        output = changePassword(apiKey, reqObj)
        return jsonify(output)