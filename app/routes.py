from flask import Flask, request, jsonify
from app.rpc_gateway import handle_rpc
from app.static_gateway import handle_static

app = Flask(__name__)

@app.route('/rpc', methods=['POST'])
def rpc():
    return handle_rpc(request)

@app.route('/static', methods=['GET'])
def static():
    return handle_static(request)
