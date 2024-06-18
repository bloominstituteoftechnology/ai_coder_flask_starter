from flask import Flask, request, jsonify, render_template, send_file
# import the agent code
import os
import shutil
from zipfile import ZipFile

app = Flask(__name__)

@app.route('/')
def Home():
    return "time2code!"


@app.route('/api/prompt', methods=['POST'])
def prompt():
    pass

@app.route('/api/download', methods=['GET'])
def download():
    pass    
    


if __name__ == '__main__':
    app.run(debug=True)

