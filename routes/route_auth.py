from service.auth.forgotPassword import forgotPassword
from service.auth.login import login
from service.auth.signup import signup
from swaggerConfig import api
from flask_restx import reqparse, Resource
from flask import jsonify, request
from service.validators.validationFunctions import validateParameters 

auth = api.namespace("auth", description="Auth Apis")

loginModel = reqparse.RequestParser()
loginModel.add_argument("username", type=str, required=True, help="Username of user", location="json")
loginModel.add_argument("password", type=str, required=True, help="Password of user", location="json")

signupModel = reqparse.RequestParser()
signupModel.add_argument("email", type=str, required=True, help="Email address", location="json")
signupModel.add_argument("password", type=str, required=True, help="Password", location="json")
signupModel.add_argument("username", type=str, required=True, help="Username of user", location="json")
signupModel.add_argument("displayName", type=str, required=True, help="Display name of user", location="json")

forgotPasswordModel = reqparse.RequestParser()
forgotPasswordModel.add_argument("email", type=str, required=True, help="Username of user", location="json")


@auth.route("/login")
class AuthLogin(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(loginModel)
    def post(self):
        reqObj = validateParameters(request.json, ["username", "password"])
        output = login(reqObj)
        return jsonify(output)

@auth.route("/signup")
class AuthSignup(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(signupModel)
    def post(self):
        print(request.remote_addr)
        reqObj = validateParameters(request.json, ["email", "password", "username", "displayName", "role"])
        output = signup(reqObj, request.remote_addr, request.environ)
        return jsonify(output)

@auth.route("/forgotPassword")
class AuthForgotPassword(Resource):
    @api.doc(responses={200: "OK"})
    @api.expect(forgotPasswordModel)
    def post(self):
        print(request.remote_addr)
        reqObj = validateParameters(request.json, ["email"])
        output = forgotPassword(reqObj, request.remote_addr, request.environ)
        return jsonify(output)
