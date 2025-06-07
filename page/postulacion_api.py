from flask import Flask, jsonify, request, send_file
from postulacion_backend import PostulacionManager
from flask_cors import CORS
from io import BytesIO
from models.model_manager import ModelManager

app = Flask(__name__)
CORS(app)  # Permitir CORS para desarrollo local

postulacion_manager = PostulacionManager()
model_manager = ModelManager()

# Variables para el modelo activo
active_model_name = None
active_model_is_deep = False

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
    # Convertir a lista de dicts para JSON
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
            'estado': p[8]
        })
    return jsonify(postulaciones_list)


@app.route('/api/models/active', methods=['GET'])
def get_active_model():
    """Devuelve información del modelo de clasificación activo."""
    if not active_model_name:
        return jsonify({})

    metadata = model_manager.load_model_metadata(active_model_name, active_model_is_deep)
    return jsonify({
        'name': active_model_name,
        'display_name': metadata.display_name if metadata else active_model_name,
        'is_deep_learning': active_model_is_deep
    })


@app.route('/api/postulaciones/cv/<int:postulacion_id>', methods=['GET'])
def download_cv(postulacion_id):
    """Descarga el archivo CV almacenado para la postulación."""
    result = postulacion_manager.download_cv(postulacion_id)
    if not result:
        return jsonify({'success': False, 'message': 'CV no encontrado'}), 404

    filename, data = result
    return send_file(BytesIO(data), download_name=filename, as_attachment=True)


@app.route('/api/postulaciones/delete/<int:postulacion_id>', methods=['DELETE'])
def delete_postulacion(postulacion_id):
    """Elimina una postulación de la base de datos."""
    success = postulacion_manager.delete_postulacion(postulacion_id)
    if success:
        return jsonify({'success': True, 'message': 'Postulación eliminada'})
    return jsonify({'success': False, 'message': 'Postulación no encontrada'}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('API_PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)
