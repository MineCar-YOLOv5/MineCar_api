import json


def Response(code, data, message):
    return json.dumps({
        "code": code,
        "data": data,
        "message": message
    })
