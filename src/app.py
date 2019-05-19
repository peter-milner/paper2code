'''Quick Start Application'''
import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from RestrictedPython import compile_restricted_exec, safe_globals
from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem
from RestrictedPython.Guards import guarded_iter_unpack_sequence

ALLOWED_EXTENSIONS = set(['jpg', 'gif', 'tiff', 'svg', 'ps'])

# pylint: disable=C0103
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@app.route('/', methods=['GET', 'POST'])
def index():
    '''Serves homepage'''
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if allowed_file(filename):
            user_input = detect_document_uri(file.read())
            output = {}
            run(user_input, output)
            user_input = user_input.replace('\n', '<br />')
            return render_template('base.html', input=user_input, result=output['out'])
    return render_template('base.html')

def run(code, output):
    '''Safely compile and run user uploaded code'''
    glb = safe_globals.copy()
    glb['_getiter_'] = default_guarded_getiter
    glb['_getitem_'] = default_guarded_getitem
    glb['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence

    try:
        byte_code = compile_restricted_exec(code)
        # pylint: disable=W0122
        exec(byte_code.code, glb, output)
    # pylint: disable=W0703
    except Exception:
        output['out'] = 'Something went wrong. Please inspect the code you entered.'

def allowed_file(filename):
    '''Verify that the filename is allowed'''
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_document_uri(img):
    """Detects document features in the file located in Google Cloud
    Storage."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image(content=img)

    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text
