from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os

'''python your_script_name.py
Now, you can access the file upload/download server from your web browser by visiting http://raspberry_pi_ip:8080/. 
You can upload files, list the uploaded files, and download them.'''

UPLOAD_FOLDER = '../data/hoerspiele'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'File uploaded successfully'
        else:
            return 'Invalid file format'
    else:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('index.html', files=files)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
