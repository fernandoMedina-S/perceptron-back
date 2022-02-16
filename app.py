import math
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

def distanciaPuntos(puntos, pesos, ubicaciones):
    distancias = {}
    indice = 0
    division_entre_cero = False
    w1_negativo = False
    w2_negativo = False
    for elemento in puntos:
        yRecta = float(pesos["w1"]) * float(elemento["offsetX"]) + float(pesos["w2"]) * float(elemento["offsetX"])

        if float(pesos["w1"]) or float(pesos["w2"])< 0:
            w1_negativo = True

        #15 = .5x + 2x
        if float(pesos["w1"]) == 0 and float(pesos["w2"]) == 0:
            xRecta = 0
            division_entre_cero = True
        else:
            try:
                xRecta = float(elemento["offsetY"]) / (float(pesos["w1"]) + float(pesos["w2"]))
            except:
                xRecta = 0   
                
        fuera = 1
        print("X dada: " + str(float(elemento["offsetX"])) + " Y dada: " + str(float(elemento["offsetY"])))
        print("X: " + str(xRecta) + " Y: " + str(yRecta))

        #and yRecta >= float(elemento["offsetY"])
        if division_entre_cero and yRecta >= float(elemento["offsetY"]):
            fuera = -1

        elif xRecta <= float(elemento["offsetX"]) and yRecta >= float(elemento["offsetY"]) and not w1_negativo:
            fuera = -1
        
        elif w1_negativo and  yRecta <= float(elemento["offsetY"]):
            fuera = -1

        
        #(Ax + Bx + C / sqrt(A^2 + B^2))
        # resultado = (float(pesos["w1"]) * float(elemento["offsetX"]) + float(pesos["w2"]) * float(elemento["offsetY"])) / (math.sqrt(math.pow(float(pesos["w1"]), 2) + math.pow(float(pesos["w2"]), 2)))
        objeto =  {"offsetX": elemento["offsetX"], "offsetY": elemento["offsetY"], "distancia": fuera, "ubicaciones": ubicaciones}
        distancias["{}".format(indice)] = objeto
        indice = indice + 1
    return distancias

@app.after_request
def after_request(response):
  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.set('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response_flask  = jsonify(response)
  response_flask.headers.add('Access-Control-Allow-Origin', '*')
  return response_flask

@app.route("/grafica", methods=["POST"])
@cross_origin()
def grafica():
    data = request.get_json()
    xValues = data["xValues"]
    puntos = data["points"]
    pesos = data["w"]
    ubicaciones = data["locations"]
    respuesta = distanciaPuntos(puntos, pesos, ubicaciones)
    return respuesta




if __name__ == "__main__":
    app.run(port = 5000, debug = False)

