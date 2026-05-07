from flask import Flask

app = Flask(__name__)

# 🔹 Importar Blueprints
from routes.backup_routes import backup_bp
from routes.restore_routes import restore_bp

# 🔹 Registrar rutas
app.register_blueprint(backup_bp)
app.register_blueprint(restore_bp)

# 🔹 Ejecutar app
if __name__ == '__main__':
    app.run(debug=True)