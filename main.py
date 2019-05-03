from flask import Flask, jsonify, request

app = Flask(__name__)

balances = {}

"""
curl localhost:5000/buy -d '{"address": "fiver", "amount": "100"}' -H 'Content-Type: application/json'
"""

@app.route('/buy', methods=['POST'])
def buy():

    args = request.get_json(force=True)

    address = args['address']
    amount = float(args['amount'])

    if address in balances:
        balances[address] += amount
    else:
        balances[address] = amount

    balances[address] = round(balances[address], 2)

    return jsonify({'OK': True})


"""
curl localhost:5000/sell -d '{"address": "fiver", "amount": "100"}' -H 'Content-Type: application/json'
"""

@app.route('/sell', methods=['POST'])
def sell():

    args = request.get_json(force=True)

    address = args['address']
    amount = float(args['amount'])

    if address in balances and balances[address] >= amount:
        balances[address] -= amount
        balances[address] = round(balances[address], 2)
        return jsonify({'OK': True})

    return jsonify({'OK': False})


@app.route('/transer', methods=['POST'])
def transfer():
    args = request.get_json(force=True)

    sender_address = args['sender_address']
    receiver_address = args['receiver_address']
    amount = float(args['amount'])

    if sender_address in balances and balances[sender_address] >= amount:
        balances[sender_address] -= amount
        if receiver_address in balances:
            balances[receiver_address] += amount
        else:
            balances[receiver_address] = amount

        balances[sender_address] = round(balances[sender_address], 2)
        balances[receiver_address] = round(balances[receiver_address], 2)

        return jsonify({'OK': True})
    return jsonify({'OK': False})

"""
curl localhost:5000/show
"""

@app.route('/show', methods=['GET'])
def show():
    return jsonify(balances)


if __name__ == '__main__':
    app.run(debug=True)
