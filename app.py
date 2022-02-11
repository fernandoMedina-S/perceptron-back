from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/grafica", methods=["POST"])
def grafica():
    puntos = request.get_json()
    print(puntos)
    print("SI")
    return "Se recibieron los puntos xd"


if __name__ == "__main__":
    app.run(port = 3030, debug = True)

