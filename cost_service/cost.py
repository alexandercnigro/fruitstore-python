#Start server
#listen on 8080

#post endpoint
#accepts body {"fruit": "pineapple"|"apple"|"kiwi"}
#else return error no valid argument, error no valid fruit, or error 500

from flask import Flask, request
import requests
from sys import argv

from fruits import fruits
# from cost_service.db import createFruit, retrieveByName, update, delete



app = Flask(__name__)
port = 9090
host = "0.0.0.0"
tax_svc_host = getTaxHost()
tax_svc_port = 9091

def getTaxHost():
    taxhostvalue="taxservice-service.default.svc.cluster.local"     # default value for local k8s cluster

    for i in range(len(argv)):
        arg=argv[i]
        if "taxhost=" in arg:
            splitarg=arg.split('=')
            taxhostvalue=splitarg[1]
            break
        elif "taxhost" in arg:
            try:
                taxhostvalue=argv[i+1]
            except:
                pass
    return taxhostvalue

@app.route('/health', methods=['GET'])
def health():
    return "Cost Service is running and healthy!"

@app.route('/cost', methods=['POST'])
def retrieveBaseCost():
    try:
        json = request.json
        base_cost = fruits[json["fruit"]]
        tax=getTax(base_cost)
        total=round(base_cost + tax, 2)
        return f"base_cost: ${base_cost:.2f}\ntax: ${tax:.2f}\ntotal: ${total:.2f}"
    except:
        #if the "fruit" key does not exist in the json
        if not request.json["fruit"]:
            raise KeyError("Key 'fruit' does not exist in the provided json.")
        
        # if the json provides a "fruit" key, but the value is not in the dictionary
        fruit = request.json["fruit"]
        if not fruits[fruit]:
            raise KeyError(f"Key '{fruit}' does not exist in fruits dictionary.")

def getTax(cost):
    req_data={"cost": f"{cost}"}
    req_headers={"Content-Type": "application/json"}
    response = requests.post(f"http://{tax_svc_host}:{tax_svc_port}/tax", headers=req_headers, json=req_data)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error. Status code {response.status_code} from Tax Service."


if __name__ == '__main__':
    if len(argv) > 1 and 'debug' in argv[1:]:
        app.run(debug=True, port=port, host=host)
    else:
        app.run(host=host, port=port)






