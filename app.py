from flask import Flask
from mighty import settings
from mighty.api import blueprint


def initialize_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.register_blueprint(blueprint)

def main():
    app = Flask(__name__)
    initialize_app(app)
    app.run(debug=True)

if __name__ == "__main__":
    main()
