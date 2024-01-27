from flask import Flask
from flask_smorest import Api

from lib.driver_setup import init_driver, shutdown_driver
from resources.order_status import blp as OrderStatusBluePrint

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = 'Orders Status API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(OrderStatusBluePrint)

if __name__ == '__main__':
    try:
        init_driver()
        app.run(debug=False)
    finally:
        shutdown_driver()
    # from waitress import serve
    # serve(app, host='0.0.0.0', port=80)
