import flask
import command
import logging
from logging import debug, info, warning, error, critical
from flask import request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
import threading
import time
import json
import shutil

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images', 'user_uploaded')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

DEFAULT_ICON_FOLDER = os.path.join("static", "images", "defaults")
os.makedirs(DEFAULT_ICON_FOLDER, exist_ok=True)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filename=os.path.join(os.path.dirname(__file__), "log.log"), filemode='a')

UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

with open('config.json', 'r') as f:
    config = json.load(f)

if config["first_start"]:
    if not os.path.exists("keys.json"):
        with open("keys.json", "w") as f:
            f.write("{}")

info("Flask app started")
debug("Initializing Flask routes")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    info("Home route accessed")
    return render_template('index.html')
  
@app.route('/control_menu')
def control_menu():
    info("control_menu route accessed")
    return render_template('control_menu.html')

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
        debug("Force shutdown executed")
        info("System shutdown command executed")
        def temp():
            time.sleep(1)
            os._exit(0)
        threading.Thread(target=temp).start()
        return render_template('shutdowning.html')
    except Exception as e:
        error(f"Error executing force shutdown: {e}")
        return render_template('noShutdown.html', error=str(e))

@app.route('/debug---test')
def debug_test():
    info("Debug test route accessed")
    return render_template('test.html')
  
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
    name = request.form.get('name', '').strip()
    if not name:
        return jsonify({"status": "error", "message": "Nom du shortcut manquant"}), 400

    chosen_icon = request.form.get('iconSelect', '').strip()

    if 'icon' in request.files and request.files['icon'].filename != '':
        file = request.files['icon']
        if not allowed_file(file.filename):
            return jsonify({"status": "error", "message": "Fichier invalide"}), 400

        filename = secure_filename(f"{name}.png")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    elif chosen_icon:
        src_path = os.path.join(DEFAULT_ICON_FOLDER, chosen_icon)
        if not os.path.exists(src_path):
            return jsonify({"status": "error", "message": "Fichier par défaut introuvable"}), 400

        filename = secure_filename(f"{name}.png")
        dest_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        shutil.copy(src_path, dest_path)
    else:
        return jsonify({"status": "error", "message": "Aucune icône sélectionnée"}), 400

    return jsonify({"status": "success", "filename": filename})

@app.route('/modifyicon')
def modify_icon():
    info("Modify icon route accessed")
    return render_template('modifyicon.html')

@app.route("/list_default_icons", methods=["GET"])
def list_default_icons():
    try:
        icons = [
            f for f in os.listdir(DEFAULT_ICON_FOLDER)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".gif"))
        ]
        return jsonify({"status": "success", "icons": icons})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route("/list_icons", methods=["GET"])
def list_icons():
    try:
        icons = [
            f for f in os.listdir(app.config['UPLOAD_FOLDER'])
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".gif"))
        ]
        return jsonify({"status": "success", "icons": icons})
    except Exception as e:
        error(f"Error listing uploaded icons: {e}")
        return jsonify({"status": "error", "message": str(e)})

debug("Flask routes initialized successfully")
info("Start app")

def commands():
    while True:
        com = input(">> ")
        if com == "exit" or com == "quit" or com == "q" or com == "stop":
            info("Exiting command loop")
            break
        elif com == "shutdown":
            info("Shutdown command received")
            shutdown()
        elif com == "force_shutdown":
            info("Force shutdown command received")
            force_shutdown()
        elif com == "reload_shortcut":
            info("Reload shortcut command received")
            reload_shortcut()
        else:
            warning("Unknown command received: %s", com)

threading.Thread(target=commands, daemon=True).start()

app.run(debug=True, host='0.0.0.0', port=config["port"])