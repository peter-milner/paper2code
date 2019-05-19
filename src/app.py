'''Quick Start Application'''
import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from RestrictedPython import compile_restricted_exec, safe_globals
from RestrictedPython.Eval import default_guarded_getiter
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
            return render_template('base.html', input=user_input, result=output['out'])
    return render_template('base.html')

def run(code, output):
    '''Safely compile and run user uploaded code'''
    glb = safe_globals.copy()
    glb['_getiter_'] = default_guarded_getiter
    glb['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
    byte_code = compile_restricted_exec(code)
    # pylint: disable=W0122
    exec(byte_code.code, glb, output)

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

    # for page in response.full_text_annotation.pages:
        # for block in page.blocks:
        #     print('\nBlock confidence: {}\n'.format(block.confidence))

        #     for paragraph in block.paragraphs:
        #         print('Paragraph confidence: {}'.format(
        #             paragraph.confidence))

        #         for word in paragraph.words:
        #             word_text = ''.join([
        #                 symbol.text for symbol in word.symbols
        #             ])
        #             print('Word text: {} (confidence: {})'.format(
        #                 word_text, word.confidence))

        #             for symbol in word.symbols:
        #                 print('\tSymbol: {} (confidence: {})'.format(
        #                     symbol.text, symbol.confidence))
