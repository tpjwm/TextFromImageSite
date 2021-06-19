import os
from flask import Flask, render_template, flash, redirect, jsonify, request, url_for
from app import app
import cv2
import pytesseract
from werkzeug.utils import secure_filename
import urllib.request


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def index_page():
    return render_template("upload.html")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route('/', methods=['POST'])
def text_extracted():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        flash('Image successfully uploaded and displayed below')
        img = cv2.imread(path)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        img_txt = pytesseract.image_to_string(img)
        return render_template('upload.html', filename=filename, img_text=img_txt)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)