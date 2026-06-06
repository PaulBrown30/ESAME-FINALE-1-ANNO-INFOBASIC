from flask import Flask
from flask_cors import CORS
from persistence.db_config import db_init
from controller.admin_controller import admin_bp
from controller.courier_controller import courier_bp
from controller.package_controller import package_bp
from controller.status_controller import status_bp
from controller.user_controller import user_bp
import samples


app = Flask(__name__)

app.register_blueprint(admin_bp)
app.register_blueprint(courier_bp)
app.register_blueprint(package_bp)
app.register_blueprint(status_bp)
app.register_blueprint(user_bp)

CORS(app)


if __name__ == "__main__":

    db_init()
    samples.create_samples()
    app.run(debug=True,port=5000)
    