import json


def Response(code, data, message):
    return json.dumps({
        "data": {
            "code": code,
            "data": data,
            "message": message
        },
    }, ensure_ascii=False)
