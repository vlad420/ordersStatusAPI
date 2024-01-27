from flask.views import MethodView
from flask_smorest import Blueprint, abort

from lib.constants import GOOGLE_CONSOLE_URL
from lib.driver_setup import get_driver, get_lock
from lib.order_status_automation import chech_if_logged_in, asteapta_logarea, get_order_status
from schemas import OrderStatusSchema

blp = Blueprint('Order Status', __name__, description='Verifica statusul comenzilor')


@blp.route('/order_status/<string:order_id>')
class OrderStatus(MethodView):
    @blp.response(200, OrderStatusSchema)
    def get(self, order_id):
        try:
            driver = get_driver()
            lock = get_lock()

            with lock:
                if not chech_if_logged_in(driver=driver):
                    driver.get(GOOGLE_CONSOLE_URL)
                    asteapta_logarea(driver=driver)

                status = get_order_status(order_id=order_id, driver=driver)
                print(f'Statusul comenzii {order_id} este: {status}')

                return OrderStatusSchema().dump({'order_id': order_id, 'status': status})
        except Exception as e:
            abort(500, message=str(e))
