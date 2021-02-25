""" Python script to parse data coming from a sensit
    Contains a handle function with context and event parameters
"""


def parse(data, version=1):
    """ Parse data for specified sensit version
    """
    if version == 1:
        parse_v1(data)

def convert_battery(data):
    ret = 0 
    if len(data) <= 2:
        ret = int(data, 16) * 0.02
    return ret

def convert_temperature(data):
    ret = 0
    if len(data) <= 2:
        ret = int(data, 16)
        if ret > 128:
            ret = ret - 256  
        ret = (ret + 46) /2 
    return ret


def parse_v1(data):
    """ Parser for sensit v1
    b0-b2: Mode (0: off, 1: temperature, 2: movement, 3: full)
    b3-b5: Period (0: 24h, 1: 12h, 2: 6h, 3: 2h, 4: 1h, 5: 30m, 6: 15m, 7: 10m)
    b6: Forced message
    b7: Button message
    B1: Battery (voltage = 0.02 * value)
    B2: Sent battery (voltage during previous frame)
    B3: Temperature = (value + 46)/2
    0-6 bytes: DATA, depend on the mode
        - Temperature: 6 values, each on 1 byte
        - Movement: 1 byte for value, 3 bytes for config
        - Full: 1 byte min temp, 1 byte max temp, 1 byte movement value
    """
    out_data = {}
    try:
        print("-- data parsing: " + str(data))
        # First byte must be split in bits
        b = "{:08b}".format(int(data[:2], base=16))
        # print("First byte: " + str(b))
        out_data.update({"mode":  int(b[2:])})
        out_data.update({"period": int(b[len(b)-5:len(b)-3], 2)})
        out_data.update({"forced": int(b[1])})
        out_data.update({"button": int(b[0])})
        # Following bytes are battery levels and temperature
        out_data.update({"battery": convert_battery(data[2:4])})
        out_data.update({"sent_battery": convert_battery(data[4:6])})
        out_data.update({"temperature": convert_temperature(data[6:8])})
        # Next bytes depends on mode
        mode = out_data.get("mode")
        out_data.update({"values": []})
        if mode == 1:
            print("-- mode temperature")
            for i in range(8, len(data), 2):
                out_data["values"].append(convert_temperature(data[i:i+2]))
        elif mode == 2:
            print("mode movement")
        elif mode == 3:
            print("mode full")
        else:
            print("OFF")
        print(out_data)
        return True
    except Exception as e:
        print("Error during data parsing " + str(data) + ". Error: " + str(e.args))
        return False


def handle(event, context):
    """ Context
    {'memoryLimitInMb': 128, 'functionName': 'sensitv1parser', 'functionVersion': ''}
    """
    """ Event
    {'resource': '',
        'path': '/',
        'httpMethod': 'POST',
        'headers': {
            'Accept-Encoding': 'gzip', 'Content-Length': '309', 'Forwarded': 'for=195.154.71.32;proto=https,
            for=100.64.7.110', 'K-Proxy-Request': 'activator', 'User-Agent': 'Go-http-client/2.0',
            'X-Envoy-Expected-Rq-Timeout-Ms': '172800000', 'X-Envoy-External-Address': '195.154.71.32',
            'X-Forwarded-For': '195.154.71.32, 100.64.7.110, 100.64.0.213', 'X-Forwarded-Proto': 'https', '
            X-Mqtt-Retain': 'false', 'X-Mqtt-Topic': 'sigfox/sensit/payload',
            'X-Request-Id': '610d2521-caac-41b8-af0cc8eddbf709fc', 'X-Request-Start': 't=1606808095.334'},
        'multiValueHeaders': None,
        'queryStringParameters': {},
        'multiValueQueryStringParameters': None,
        'pathParameters': None,
        'stageVariables': {},
        'requestContext': {
            'accountId': '', 'resourceId': '', 'stage': '', 'requestId': '', 'resourcePath': '',
            'authorizer': None, 'httpMethod': 'POST', 'apiId': ''},
        'body': '{\r\n "data": "01b7b6010101010101",
            \r\n "id": "B92A4",
            \r\n "customData#Modes": "1",
            \r\n "customData#bat": "-73",
            \r\n "customData#batEnv": "-74",
            \r\n "customData#tempbase": "1",
            \r\n "time": "1606808070",
            \r\n "computedLocation": {
                "lat":42.92188741630114, "lng":1.5906386969099215,
                "radius":30200, "source":2,"status":1}\r\n
                }'
    }
    """
    print("Message from " + str(event.get("resource",{}).get("body", {}).get("id")) +". Data: " \
     + str(event.get("body", {}).get("data")))
    parse(data=event.get("body", {}).get("data", ""))
    return {"body": {"message": 'Hello, world' }, "statusCode": 200 }


