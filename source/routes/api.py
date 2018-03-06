from flask import Flask, jsonify, abort, request

app = Flask(__name__)

app.config['SECRET_KEY']="b'409ce0cacf23b39b71faccfcb2f9fc3051c587d6155efa77'"
"""
Enables use of token

"""
@app.route('/api/auth/v1/register', methods=['POST'])
def get_routes():
    pass