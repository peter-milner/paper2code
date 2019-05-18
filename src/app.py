'''Quick Start Application'''
import os

from flask import Flask

# pylint: disable=C0103
app = Flask(__name__)

@app.route('/')
def hello_world():
    '''Serves hello world'''
    target = os.environ.get('TARGET', 'World')
    return 'Hello {}!\n'.format(target)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
