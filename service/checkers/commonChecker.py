from models.conn import userCollections


def pageChecker(response, page):
    if page != None:
        if page.isdigit():
            if int(page) > 0:
                return True, int(page)
            else:
                response.setStatus(400)
                response.setError("Page cannot be 0")
                return False, None
        else:
            response.setStatus(400)
            response.setError("Invalid page number passed")
            return False, None
    else:
        return True, 1


def queryChecker(response, query):
    if query != None:
        if len(query) >= 3:
            return True, query
        else:
            response.setStatus(400)
            response.setError("Query parameter should be more then 2 character")
            return False, None
    else:
        response.setStatus(400)
        response.setError("Query does not passed")
        return False, None


def emailCheckerForSignup(response, email):
    if email != None:
        emailCheck = userCollections.count_documents({"email" : email.lower()})
        if emailCheck == 0:
            return True, email.lower()
        else:
            response.setStatus(400)
            response.setError("Email is already in use")
            return False, None
    else:
        response.setStatus(400)
        response.setError("Email does not provided")
        return False, None


def usernameCheckerForSignup(response, username):
    if username != None:
        usernameCheck = userCollections.count_documents({"username" : username.lower()})
        if usernameCheck == 0:
            return True, username.lower()
        else:
            response.setStatus(400)
            response.setError("Username is already taken")
            return False, None
    else:
        response.setStatus(400)
        response.setError("Username does not provided")
        return False, None


def passwordChecker(response, password):
    if password != None:
        if len(password) >= 8:
            return True, password
        else:
            response.setStatus(400)
            response.setError("Password length should be atleast 8 character")
            return False, None
    else:
        response.setStatus(400)
        response.setError("Password does not provided")
        return False, None


def displayNameChecker(response, displayName):
    if displayName != None:
        if displayName != "":
            return True, displayName
        else:
            response.setStatus(400)
            response.setError("Invalid display name")
            return False, None
    else:
        response.setStatus(400)
        response.setError("Display name not provided")
        return False, None


def emailCheckerForLogin(response, email):
    if email != None:
        emailCheck = userCollections.count_documents({"email" : email.lower()})
        if emailCheck == 0:
            return True, email.lower()
        else:
            response.setStatus(400)
            response.setError("Email is already in use")
            return False, None
    else:
        response.setStatus(400)
        response.setError("Email does not provided")
        return False, None


def usernameCheckerForLogin(response, username):
    if username != None:
        userObj = userCollections.find_one({"username" : username.lower()})
        if userObj:
            return True, userObj
        else:
            response.setStatus(404)
            response.setError("Username is does not found")
            return False, None
    else:
        response.setStatus(400)
        response.setError("Username does not provided")
        return False, None