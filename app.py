from flask import Flask
from mighty import settings
from mighty.api import blueprint

app = Flask(__name__)

app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
app.register_blueprint(blueprint)

def main():
    app.run(port=8080, debug=True)

if __name__ == "__main__":
    main()
