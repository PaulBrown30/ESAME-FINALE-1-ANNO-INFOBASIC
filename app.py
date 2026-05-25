from flask import Flask
from flask_cors import CORS
from persistence.db_config import db_init




app = Flask(__name__)

if __name__ == "__main__":

    db_init()
    app.run(debug=True,port=5000)