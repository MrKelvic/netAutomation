import helpers.getInventary as getInventary 
import functions.config2code as genState
import functions.code2config as digest
import functions.engineBase as engineInteractor
import helpers.writeToExcel as writeToExcel



import json
from flask import Flask,jsonify, request,send_file
from flask_cors import CORS, cross_origin
PORT=8001
host="0.0.0.0"
app = Flask(__name__) 
cors = CORS(app)

def index():
    app.run(host=host,debug=True, port=PORT)

""" POST """

# ENDPOINT
@app.route("/engine",methods=["POST"])
@cross_origin()
def engine():
    httpParams=request.get_json() or {}
    nodes=httpParams['nodes'] if 'nodes' in httpParams else []
    engineFn=httpParams['engineFn'] if 'engineFn' in httpParams else "info"
    action=httpParams['action'] if 'action' in httpParams else "get"
    params=httpParams['params'] if 'params' in httpParams else []
    # print(nodes)
    # filter = request.args.get('filter', default = 0, type = int)
    # type=action
    actionResults=engineInteractor.index(nodes=nodes,engineFn=engineFn,params=params)
    httpRes=[]
    for eng in actionResults:
        httpRes.append({
            "web":eng.web,
            "cli":eng.cli,
            "output":eng.output,
            "node":eng.node,
        })
    return json.dumps(httpRes)

# ENDPOINT REPORT GENARATORS
@app.route("/report",methods=["POST","GET"])
@cross_origin()
def report():
    filePath = request.args.get('path', default = None, type = str)
    print(filePath)
    try:
        if filePath:
            splittedValues=filePath.split("/")
            nameOfFile=splittedValues.pop()
            if '-'.join(splittedValues) == 'store-temp-reports':
                return send_file("../"+filePath,as_attachment=True,download_name='AutomatedReport'+nameOfFile)
            else:
                return "Opps"
        else:
            httpParams=request.get_json() or {}
            payload=httpParams['payload']
            if not payload:
                raise Exception("PROVIDE DATA TO GENERATE REPORT")
            filePath=writeToExcel.getReport(payload)
            # print(request.url_root)
            print("Path:: ",request.url_root+"report?path="+filePath)
            return json.dumps({
                "path":request.url_root+"report?path="+filePath
            })
    except Exception as error:
        print(error)
        return "Hi"






# ENDPOINT
@app.route("/inventory",methods=["GET"])
@cross_origin()
def inventory():
    filter = request.args.get('filter', default = 0, type = int)
    return json.dumps(getInventary.getDevices(filter))

@app.route("/inventory",methods=["POST"])
@cross_origin()
def addInventory():
    httpParams=request.get_json() or {}
    payload=httpParams['device']
    getInventary.addDevice(payload)
    return json.dumps(getInventary.getDevices(0))

@app.route("/inventory",methods=["PUT"])
@cross_origin()
def updateInventory():
    httpParams=request.get_json() or {}
    payload=httpParams['device']
    getInventary.updateDevice(payload)
    return json.dumps(getInventary.getDevices(0))

@app.route("/inventory",methods=["DELETE"])
@cross_origin()
def deleteInventory():
    httpParams=request.get_json() or {}
    payload=httpParams['ip']
    getInventary.deleteDevice(payload)
    return json.dumps(getInventary.getDevices(0))



# ENDPOINT
@app.route("/intent",methods=["GET"])
@cross_origin()
def intent():
    state = request.args.get('state', default = 'OSPF1_192.168.122.230', type = str)
    node=getInventary.findDevice(state.split("_")[1])
    return json.dumps({
        "node":node,
        "state":getInventary.getState(state)
    })


# ENDPOINT
@app.route("/state",methods=["GET"])
@cross_origin()
def state():
    ip = request.args.get('ip', default = '192.168.122.230', type = str)
    node=getInventary.findDevice(ip)
    if not node:
        return {}
    return json.dumps(genState.index([node],write=False))

# ENDPOINT
@app.route("/digestChanges",methods=["POST"])
@cross_origin()
def digestChanges():
    httpParams=request.get_json() or {}
    code=httpParams['code']
    node=httpParams['node']
    # print(code)
    # getInventary.addDevice(payload)
    return json.dumps(digest.index(code,node))



if __name__ == '__main__':
    index()