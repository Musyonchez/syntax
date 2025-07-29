# Auth Function Shell
# Google OAuth + JWT authentication
# Port: 8081

from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'auth'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)