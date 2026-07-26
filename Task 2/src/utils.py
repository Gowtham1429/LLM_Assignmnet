import json

def parse_json(text):
    try:
        return json.loads(text)
    except:
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end + 1])
            except:
                pass

    return None
