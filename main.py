from flask import Flask
from routes.backup_routes import backup_bp
from routes.restore_routes import restore_bp

app = Flask(__name__)

app.register_blueprint(backup_bp)

app.register_blueprint(restore_bp)

if __name__ == '__main__':

    app.run(debug=True)