def validateParameters(requestData, checkDetail):
    outputObj = {}
    for i in checkDetail:
        outputObj[i] = requestData.get(i)

    return outputObj