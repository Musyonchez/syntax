# Practice Function Shell
# Practice sessions + scoring
# Port: 8082

from flask import Flask

app = Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'ok', 'service': 'practice'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True)