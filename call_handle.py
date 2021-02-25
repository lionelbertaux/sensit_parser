import sensit_parser
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--data", default="01b7b6010101010101", help="Data sent by device")
args = ap.parse_args()

sensit_parser.handle(context={}, event={"body":{"data": args.data}})
