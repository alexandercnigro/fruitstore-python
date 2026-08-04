from flask import Flask, request
from sys import argv

app = Flask(__name__)
port=9091
host="0.0.0.0"


@app.route('/health', methods=['GET'])
def health():
    return "Tax Service is running and healthy!"

@app.route('/tax', methods=['POST'])
def retrieveTax():
    cost = float(request.json["cost"])
    tax = round(cost * 0.05, 2)
    return str(tax)


if __name__ == '__main__':
    if len(argv) > 1 and 'debug' in argv[1:]:
        app.run(debug=True, port=port, host=host)
    else:
        app.run(host=host, port=port)







