from flask import Flask, jsonify, request

app = Flask(__name__)

database = {}
database_ips = {}

@app.route('/login', methods=['POST'])
def login():
    global database
    global database_ips
    data = request.json
    peer_id = data['user']
    peer_pass = data["password"]
    peer_ip = data["ip"]
    database[peer_id] = {}
    database_ips[peer_id] = peer_ip
    return jsonify({'message': 'Login successful', 'peer_id': peer_id, 'peer_password': peer_pass, ' ip:': peer_ip}), 200

@app.route('/logout', methods=['POST'])
def logout():
    global database
    global database_ips
    data = request.json
    peer_id = data['user']
    if peer_id in database:
        del database[peer_id]
        del database_ips[peer_id]
        return jsonify({'message': 'Logout successful', 'peer_id': peer_id}), 200
    else:
        return jsonify({'error': 'Peer not found'}), 404

@app.route('/index', methods=['POST'])
def index():
    global database
    global database_ips
    data = request.json
    peer_id = data['user']
    port = data['port']
    if peer_id in database:
        files = data['files']
        database[peer_id]['files'] = files
        database_ips[peer_id] = port
        return jsonify({'message': 'Indexing successful', 'peer_id': peer_id, 'files': files}), 200
    else:
        return jsonify({'message': 'This peer does not exist ', 'peer_id': peer_id}), 404

@app.route('/search', methods=['GET'])
def search():
    global database
    global database_ips
    filename = request.args.get('filename')
    for peer_id, info in database.items():
        print(peer_id, " ", info)
        if 'files' in info and filename in info['files']:
            return jsonify({'message': 'File found', 'user': peer_id, 'filename': filename, 'port': database_ips[peer_id]}), 200
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
