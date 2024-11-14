from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import pandas as pd
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

# Pasta para salvar arquivos temporários
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'csv', 'json', 'xml'}

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Função para limpar os arquivos depois de processados (opcional)
def clean_up(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Erro ao remover arquivo {file_path}: {e}")

# Rota para upload de arquivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        data = {}

        try:
            # Processar o arquivo conforme a extensão
            if file_extension == 'json':
                with open(filename, 'r') as f:
                    data = json.load(f)
                clean_up(filename)

            elif file_extension == 'csv':
                data = pd.read_csv(filename).to_dict(orient='records')  # Usando 'records' para retorno em formato lista de dicionários
                clean_up(filename)

            elif file_extension == 'xml':
                tree = ET.parse(filename)
                root = tree.getroot()
                data = {root.tag: [elem.tag for elem in root]}
                clean_up(filename)

            elif file_extension == 'txt':
                with open(filename, 'r') as f:
                    data = f.read()
                clean_up(filename)

            return jsonify({"data": data})

        except Exception as e:
            clean_up(filename)
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500

    return jsonify({"error": "File extension not allowed"}), 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
