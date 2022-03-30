import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from luma_tools import convert_bf_to_neticrm
from shutil import rmtree
from datetime import datetime

UPLOAD_FOLDER = os.getcwd() + '/csv'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #rebuild temp folder
            if os.path.isdir(app.config['UPLOAD_FOLDER']):
                rmtree(app.config['UPLOAD_FOLDER'])
            os.mkdir(app.config['UPLOAD_FOLDER'])
            #save original csv
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #prepare new csv file name
            now = datetime.now()
            rukai_filename = filename.replace('.csv','_rukau.csv')
            converted_filename = filename.replace('.csv','_neticrm_' + now.strftime('%y%m%d%H%M%S') + '.csv')
            convert_bf_to_neticrm(UPLOAD_FOLDER + '/' + filename, UPLOAD_FOLDER + '/' + converted_filename)
            return redirect(url_for('download_file', name=converted_filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>請上傳貝殼放大CSV匯出檔</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

from flask import send_from_directory

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

if __name__ == '__main__':
    app.run()