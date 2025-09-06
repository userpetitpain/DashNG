import flask
import command
import logging
from logging import debug, info, warning, error, critical
from flask import request, jsonify, render_template
import os
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'icons')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename='log.log', filemode='a')

UPLOAD_FOLDER = "static/icons"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

info("Flask app started")
debug("Initializing Flask routes")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    info("Home route accessed")
    return render_template('index.html')
  
@app.route('/zackcarplay')
def zackcarplay():
    info("ZackCarPlay route accessed")
    return render_template('zackcarplay.html')

@app.route('/reload_shortcut')
def reload_shortcut():
    command.repair_cached_shortcuts()
    
@app.route('/control')
def control():
    info("Control route accessed")
    return render_template('control.html')
    
@app.route('/shutdown')
def shutdown():
    info("Shutdown route accessed")
    if request.environ.get('werkzeug.server.shutdown'):
        request.environ.get('werkzeug.server.shutdown')()
        info("Server shutdown initiated")
        return render_template('shutdowning.html')
    else:
        error("Server shutdown not supported in this environment")
        return render_template('noShutdown.html')
    
@app.route('/force_shutdown')
def force_shutdown():
    info("Force shutdown route accessed")
    try:
        os._exit(0)
        debug("Force shutdown executed")
        info("System shutdown command executed")
        return render_template('shutdowning.html')
    except Exception as e:
        error(f"Error executing force shutdown: {e}")
        return render_template('noShutdown.html', error=str(e))
  
@app.route('/settings')
def settings():
    info("Settings route accessed")
    return render_template('settings.html')

@app.route('/settings/list_shortcuts', methods=['GET'])
def list_shortcuts():
    info("List shortcuts route accessed")
    try:
        command.repair_cached_shortcuts()
        shortcuts = command.list_shortcuts()
        debug(f"Shortcuts retrieved: {shortcuts}")
        return jsonify({'status': 'success', 'shortcuts': shortcuts})
    except Exception as e:
        error(f"Error retrieving shortcuts: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route("/settings/add_shortcut", methods=['POST'])
def add_shortcut():
    data = request.get_json()
    name = data.get('name')
    actions = data.get('actions')

    if not name or not actions:
        return jsonify({"status": "error", "message": "Missing name or actions"}), 400

    command.add_shortcut(name, actions)
    debug(f"Shortcut added: {name} -> {actions}")

    return jsonify({"status": "success", "shortcut": {name: actions}})
@app.route('/settings/remove_shortcut', methods=['POST'])
def remove_shortcut():
    data = request.get_json()
    name = data.get('name')

    command.remove_shortcut(name)
    debug(f"Shortcut removed: {name}")

    return jsonify({"status": "success", "shortcut": name})

@app.route('/execute_shortcut', methods=['POST'])
def execute_shortcut():
    data = request.get_json()
    shortcut = data.get('shortcut')

    if not shortcut:
        return jsonify({"status": "error", "message": "Missing shortcut"}), 400

    try:
        command.execute(shortcut)
        debug(f"Executed shortcut: {shortcut}")
        return jsonify({"status": "success", "shortcut": shortcut})
    except Exception as e:
        error(f"Error executing shortcut: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/upload_icon', methods=['POST'])
def upload_icon():
    if 'icon' not in request.files or 'name' not in request.form:
        return jsonify({"status": "error", "message": "No file or name provided"}), 400

    file = request.files['icon']
    name = request.form['name'].strip()
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"status": "error", "message": "Invalid file"}), 400
    
    filename = secure_filename(f"{name}.png")  # renomme le fichier pour correspondre au nom de l'app
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    return jsonify({"status": "success", "filename": filename})

@app.route('/modifyicon')
def modify_icon():
    info("Modify icon route accessed")
    return render_template('modifyicon.html')
    
# @app.route('/test_shortcut', methods=['GET', 'POST'])
# def test_shortcut():
#     info("Test shortcut route accessed")
#     try:
#         if request.method == 'POST':
#             # Récupère les actions depuis le JSON
#             data = request.get_json()
#             actions = data.get('actions', [])
#             debug(f"POST actions received: {actions}")
            
#             # Exécute les actions (à adapter selon ton système)
#             for action in actions:
#                 if isinstance(action, list):
#                     action_str = '+'.join(action)
#                 else:
#                     action_str = str(action)
#                 command.execute(action_str)
#                 debug(f"Command executed: {action_str}")
            
#         return jsonify({'status': 'success', 'message': 'Action triggered successfully'})
#     except Exception as e:
#         error(f"Error executing command: {e}")
#         return jsonify({'status': 'error', 'message': str(e)}), 500

debug("Flask routes initialized successfully")
info("Start app")

app.run(debug=True, host='0.0.0.0', port=8923)