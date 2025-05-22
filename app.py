# app.py
from flask import Flask, render_template, request, jsonify
from detector import detect_and_read_plate
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    plate_text = detect_and_read_plate(filepath)

    return jsonify({'plate': plate_text})

# This block is only used for local testing. Render uses gunicorn.
# if __name__ == '__main__':
#    app.run(debug=True)
