def getApiKey(request):
    return request.headers.get("X-Api-Key")