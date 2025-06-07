from flask import Flask, jsonify, request, send_file
from postulacion_backend import PostulacionManager
from postulacion_extension import add_classification_columns
from flask_cors import CORS
from io import BytesIO
import joblib
from PyPDF2 import PdfReader
import threading
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.model_manager import ModelManager
from models.cv_classifier import CVClassifier
from models.deep_learning_classifier import DeepLearningClassifier
from src.config.settings import Settings

app = Flask(__name__)
CORS(app)  # Permitir CORS para desarrollo local

# Asegurar que la base de datos tenga las columnas de clasificación
add_classification_columns()

postulacion_manager = PostulacionManager()
model_manager = ModelManager()

# Variables globales para el modelo activo
active_model_name = None
active_model_is_deep = False
active_classifier = None
active_classifier_lock = threading.Lock()


def extract_text_from_pdf(pdf_bytes):
    """Extrae texto de un PDF en bytes usando PyPDF2"""
    text = ""
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    except Exception as exc:
        raise ValueError(f"Error extrayendo texto del PDF: {exc}")
    return text


def load_active_model():
    """Carga el modelo activo en memoria"""
    global active_classifier
    if active_model_name is None:
        active_classifier = None
        return
    if active_model_is_deep:
        classifier = DeepLearningClassifier()
    else:
        model_dir = Settings.MODELS_DIR
        classifier = CVClassifier(model_dir=str(model_dir))

    success = classifier.load_model(active_model_name)
    active_classifier = classifier if success else None

@app.route('/api/postulaciones', methods=['GET', 'POST'])
def handle_postulaciones():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        dni = request.form.get('dni')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        cv_file = request.files.get('cv')

        if not all([nombre, dni, correo, telefono, cv_file]):
            return jsonify({'success': False, 'message': 'Faltan datos en el formulario.'}), 400

        if not cv_file.filename:
            return jsonify({'success': False, 'message': 'No se ha subido ningún archivo CV.'}), 400

        cv_filename = cv_file.filename
        cv_data = cv_file.read()

        result = postulacion_manager.process_postulacion(nombre, dni, telefono, correo, cv_filename, cv_data)

        if result.get('success'):
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    
    # Manejo para GET
    postulaciones = postulacion_manager.get_postulaciones_list()
    postulaciones_list = []
    for p in postulaciones:
        postulaciones_list.append({
            'id': p[0],
            'nombre': p[1],
            'dni': p[2],
            'telefono': p[3],
            'correo': p[4],
            'cv_filename': p[5],
            'cv_size': p[6],
            'fecha_postulacion': p[7],
            'estado': p[8],
            'puesto_clasificacion': p[9] if len(p) > 9 else '',
            'porcentaje_clasificacion': p[10] if len(p) > 10 else 0.0,
            'modelo_clasificacion': p[11] if len(p) > 11 else ''
        })
    return jsonify(postulaciones_list)


@app.route('/api/models', methods=['GET'])
def list_models():
    ml_classifier = CVClassifier()
    ml_models = ml_classifier.list_available_models()

    dl_models = []
    saved_dl_dir = Settings.DEEP_MODELS_DIR
    if os.path.exists(saved_dl_dir):
        for model_name in os.listdir(saved_dl_dir):
            model_path = os.path.join(saved_dl_dir, model_name)
            if os.path.isdir(model_path):
                metadata_file = None
                for candidate in ['package_info.json', 'senati_info.json']:
                    candidate_path = os.path.join(model_path, candidate)
                    if os.path.isfile(candidate_path):
                        metadata_file = candidate_path
                        break
                if metadata_file:
                    try:
                        with open(metadata_file, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                        dl_models.append({
                            'name': model_name,
                            'display_name': metadata.get('model_name', model_name),
                            'model_type': 'dl',
                            'creation_date': metadata.get('creation_date', ''),
                            'description': metadata.get('description', ''),
                            'is_deep_learning': True,
                            'num_professions': metadata.get('num_professions', 0),
                            'model_format': metadata.get('format_version', 'unknown'),
                            'num_features': metadata.get('num_features', 'N/A'),
                            'hyperparameters': metadata.get('hyperparameters', {})
                        })
                    except Exception:
                        pass

    combined_models = ml_models + dl_models

    def get_creation_date(model):
        return model.get('creation_date', '') or ''

    combined_models.sort(key=get_creation_date, reverse=True)
    return jsonify(combined_models)


@app.route('/api/models/select', methods=['POST'])
def select_model():
    global active_model_name, active_model_is_deep
    data = request.json
    model_name = data.get('model_name')
    is_deep = data.get('is_deep', False)
    if not model_name:
        return jsonify({'success': False, 'message': 'model_name es requerido'}), 400
    active_model_name = model_name
    active_model_is_deep = is_deep
    load_active_model()
    return jsonify({'success': True, 'message': f'Modelo {model_name} seleccionado'})


@app.route('/api/models/active', methods=['GET'])
def get_active_model():
    """Devuelve información del modelo activo"""
    if not active_model_name:
        return jsonify({})
    model_dir = Settings.DEEP_MODELS_DIR if active_model_is_deep else Settings.MODELS_DIR
    metadata_path = os.path.join(model_dir, active_model_name, 'metadata.pkl')
    display_name = active_model_name
    if os.path.exists(metadata_path):
        try:
            metadata = joblib.load(metadata_path)
            display_name = metadata.get('model_name', active_model_name)
        except Exception:
            pass
    return jsonify({
        'name': active_model_name,
        'display_name': display_name,
        'is_deep_learning': active_model_is_deep
    })


@app.route('/api/postulaciones/classify/<int:postulacion_id>', methods=['POST'])
def classify_postulacion(postulacion_id):
    global active_classifier, active_model_name
    if active_classifier is None:
        return jsonify({'success': False, 'message': 'No hay modelo activo cargado'}), 400
    postulacion = postulacion_manager.get_postulacion_details(postulacion_id)
    if not postulacion:
        return jsonify({'success': False, 'message': 'Postulación no encontrada'}), 404
    cv_data = postulacion_manager.download_cv(postulacion_id)
    if not cv_data:
        return jsonify({'success': False, 'message': 'CV no encontrado'}), 404
    _, cv_bytes = cv_data
    try:
        cv_text = extract_text_from_pdf(cv_bytes)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    result = active_classifier.predict_cv(cv_text)
    if result.get('error'):
        return jsonify({'success': False, 'message': result.get('message')}), 500

    puesto = result.get('predicted_profession', '')
    porcentaje = result.get('confidence', 0.0)
    try:
        update_classification_result(postulacion_id, puesto, porcentaje, active_model_name)
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error guardando resultado: {str(e)}'}), 500
    return jsonify({'success': True, 'puesto': puesto, 'porcentaje': porcentaje, 'modelo': active_model_name})


@app.route('/api/postulaciones/cv/<int:postulacion_id>', methods=['GET'])
def download_cv(postulacion_id):
    """Devuelve el archivo CV guardado"""
    cv_data = postulacion_manager.download_cv(postulacion_id)
    if not cv_data:
        return jsonify({'success': False, 'message': 'CV no encontrado'}), 404
    filename, data = cv_data
    return send_file(BytesIO(data), download_name=filename, as_attachment=True)


@app.route('/api/postulaciones/delete/<int:postulacion_id>', methods=['DELETE'])
def delete_postulacion(postulacion_id):
    """Elimina una postulación"""
    success = postulacion_manager.delete_postulacion(postulacion_id)
    if success:
        return jsonify({'success': True, 'message': 'Postulación eliminada'})
    return jsonify({'success': False, 'message': 'No se pudo eliminar'}), 400


def update_classification_result(postulacion_id, puesto, porcentaje, modelo):
    import sqlite3
    DATABASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database')
    DATABASE_NAME = "postulaciones.db"
    DATABASE_PATH = os.path.join(DATABASE_DIR, DATABASE_NAME)
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE postulaciones
            SET puesto_clasificacion = ?, porcentaje_clasificacion = ?, modelo_clasificacion = ?
            WHERE id = ?
            """,
            (puesto, porcentaje, modelo, postulacion_id),
        )
        conn.commit()
    finally:
        if conn:
            conn.close()


def start_server(port=5000):
    """Inicia el servidor Flask"""
    app.run(host='0.0.0.0', debug=True, port=port)


def start_server_thread(port=5000):
    """Inicia el servidor en un hilo separado"""
    thread = threading.Thread(target=start_server, kwargs={'port': port}, daemon=True)
    thread.start()
    return thread

if __name__ == '__main__':
    port = int(os.environ.get('API_PORT', 5000))
    start_server(port)
