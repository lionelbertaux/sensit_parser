""" Python script to parse data coming from a sensit
    Contains a handle function with context and event parameters

    Author: Lionel Bertaux
    Date: 23/04/2021
    Version: 1.0
    Github repo: https://github.com/lionelbertaux/sensit_parser.git
"""

import json

def parse(data, version=1):
    """ Parse data for specified sensit version
    """
    if version == 1:
        ret = parse_v1(data)
    else:
        ret = {"body": {"message": "version not supported"}, "statusCode": 500}
    return ret

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
            print("-- Data parsed: " + str(out_data))
            return {"body": {"message": "Temperature message stored " + str(out_data.get("values"))}, "statusCode": 200}
        elif mode == 2:
            print("mode movement")
            return {"body": {"message": "Mouvement message not implemented yet"}, "statusCode": 500}

        elif mode == 3:
            print("mode full")
            return {"body": {"message": "Full message not implemented yet"}, "statusCode": 500}
        else:
            print("OFF")
            return {"body": {"message": "OFF notification not implemented yet"}, "statusCode": 500}
    except Exception as e:
        print("Error during data parsing " + str(data) + ". Error: " + str(e.args))
        return {"body": {"message": "Error " + str(e.args)}, "statusCode": 500}
    return {"body": {"message": "Nothing was processed"}, "statusCode": 500}

def handle(event, context):
    if event.get("httpMethod") != "POST":
        return {"body": {"message": "Only POST method is allowed"}, "statusCode": 501}
    body = event.get("body", {})
    if body == {}:
        return {"body": {"message": "Body of request not found"}, "statusCode": 500}
    # The body is given as a string
    if type(body) == str:
        body = json.loads(body)
    ret = parse(data=body.get("data", ""), version=1)
    return ret
