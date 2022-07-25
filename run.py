from flask import Flask

from app.main import main_blueprint

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
