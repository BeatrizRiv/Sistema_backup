from flask import Flask
from config import FLASK_SECRET_KEY
from routes.auth_routes import auth_bp
from routes.backup_routes import backup_bp
from routes.restore_routes import restore_bp
from utils.backup_scheduler import iniciar_backup_automatico

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(backup_bp) 
app.register_blueprint(restore_bp)

if __name__ == '__main__':

    iniciar_backup_automatico()
    app.run(debug=True)