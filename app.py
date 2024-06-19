from flask import Flask, request, jsonify, render_template, send_file
from agent_code import agent_executor

# import the agent code
import os
import shutil
from zipfile import ZipFile

app = Flask(__name__)

ZIP_DIR = os.path.join('./', 'app')

@app.route('/')
def Home():
    return render_template('index.html')


@app.route('/api/prompt', methods=['POST'])
def prompt():
    data = request.json
    user_prompt = data.get('prompt') + "\n Make sure to create a directory called app to put the files in to." 
    response = list(agent_executor.stream({"input": user_prompt}))
    return "App Created Successfully!"

@app.route('/api/download', methods=['GET'])
def download():
    zip_path = 'app.zip'

    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    with ZipFile(zip_path, 'w') as zip_file:
        for root, dirx, files in os.walk(ZIP_DIR):
            for file in files:
                zip_file.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                           os.path.join(ZIP_DIR, '..')))
    
    try:
        shutil.rmtree(ZIP_DIR)
    except Exception as e:
        return jsonify(error=f"Failed to delete directory '{ZIP_DIR}': {e}")
    
    return send_file(zip_path, as_attachment=True)
    


if __name__ == '__main__':
    app.run(debug=True, port=5050)

