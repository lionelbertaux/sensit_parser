import sensit_parser
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--data", default="01b7b6010101010101", help="Data sent by device")
args = ap.parse_args()

ret = sensit_parser.handle(context={}, event={"httpMethod": "POST", "body":{"data": args.data}})
print(ret)
