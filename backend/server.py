from flask import Flask, request
import helper_functions

app = Flask(__name__)

@app.route("/get")
def get_endpoint():

    addr = request.args.get("addr")
    date = request.args.get("date")
    print(date)
    data = helper_functions.get_iata_code_from_address(addr, date)
    return data


app.run()


    