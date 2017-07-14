from flask import Flask, jsonify, request
from Manager.proxyManager import ProxyManager
app = Flask(__name__)
api_list = {
    'get':'get an usable proxy',
    'refresh': 'refresh proxy pool',
    'get_all': 'get all proxy from proxy pool',
    'delete?proxy=127.0.0.1:8000':'delete an unable proxy'
}

@app.route('/')
def index():
    return jsonify(api_list)

@app.route('/get/')
def get():
    proxy = ProxyManager().get()
    return jsonify(proxy.decode('utf-8') if isinstance(proxy,bytes) else proxy)

@app.route('/refresh/')
def refresh():
    # ProxyManager().refresh()
    return "Refresh success"

@app.route('/get_all/')
def get_all():
    proxies = [proxy.decode('utf-8') for proxy in ProxyManager().getAll() if isinstance(proxy,bytes)]
    return jsonify(proxies)

@app.route('/delete/',methods=['GET'])
def delete():
    proxy = request.args.get('prxoy')
    ProxyManager().delete(proxy)
    return "Delete {proxy} success".format(proxy=proxy)

def run():
    app.run(host="localhost",port='5000')

if __name__ == '__main__':
    run()