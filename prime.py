import uuid
from flask import Flask, jsonify, request

instance_id = uuid.uuid4().hex

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def get_instance_id():
    if (request.method == "POST"):
        some_json = request.get_json()
        return jsonify({'Processing': some_json})
    else:
        return jsonify({'InstanceID': instance_id,
                        'Message': 'Autobots, fall back now!'})


@app.route('/number/<int:num>', methods=['GET'])
def is_prime(num):
    if num > 1:
        for i in range(2, int(num/2)+1):
            if (num % i) == 0:
                return jsonify({'Message': 'Optimus says it is Not a Prime'})
            else:
                return jsonify({'Message': 'Optimus says it is a Prime'})

    return jsonify({'Message': 'Optimus says it is Not a Prime'})


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
