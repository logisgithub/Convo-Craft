from flask import Flask,render_template, redirect, url_for, request
import subprocess
from resume import extractDetails

app=Flask(__name__)

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html')

@app.route('/interview')

def interview():
    return render_template('interview.html')

@app.route('/speech_bot')

def speech_bot():
    try:
        subprocess.run(['python', 'testingchatbot.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return redirect(url_for('index'))


@app.route('/verbal')

def verbal():
    return render_template('verbal.html')

@app.route('/hometoverbal')

def hometoverbal():
    return render_template('landingpage2.html')

@app.route('/hometointerview')

def hometointerview():
    return render_template('landingpage1.html')

@app.route('/hometoresume')

def hometoresume():
    return render_template('landingpage3.html')

@app.route('/verbal_bot')

def verbal_bot():
    try:
        subprocess.run(['python', 'verbal.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return redirect(url_for('index'))

@app.route('/upload')

def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])

def upload_file():
    if 'pdfFile' not in request.files:
        return 'No file uploaded', 400

    file = request.files['pdfFile']
    if file.filename == '':
        return 'No selected file', 400

    # Process the file
    file_path = 'E:\ResumeAnalyzer\Resumes' + file.filename
    file.save(file_path)
    
    extractDetails(file_path)

    return redirect(url_for('hometoresume'))

@app.route('/resumeinterview')

def resumeinterview():
    return render_template('resumeinterview.html')

@app.route('/resume_interview')

def resume_interview():
    try:
        subprocess.run(['python', 'resumeinterview.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    return redirect(url_for('index'))

@app.route('/login')

def login():
    return render_template('login.html')


@app.route('/report')

def report():
    return render_template('report.html')

if __name__=='__main__':
    app.run(debug=True)