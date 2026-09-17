from todosar.celery import app
from orders.models import Order, TNCallback
from orders.choices import Status
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def save_order_change(bk_code, item_id, topic):
    status_map = {
        "order/paid": Status.PAID,
        "order/packed": Status.SHIPPED,
        "order/fulfilled": Status.COMPLETED,
        "order/cancelled": Status.CANCELLED,
    }

    if Order.objects.filter(order_id=item_id).exists():
        order = Order.objects.get(order_id=item_id)
        order.status = status_map.get(topic)
        order.save()


@app.task()
def save_tn_callbacks(data):
    actions = {
        "order/paid": save_order_change,
        "order/packed": save_order_change,
        "order/fulfilled": save_order_change,
        "order/cancelled": save_order_change,
    }
    tn_call = TNCallback.objects.create(
        store_id=data["store_id"],
        topic=data["event"],
        item_id=data["id"],
        content=data,
    )
    try:
        actions[data["event"]](data["store_id"], data["id"], data["event"])
        tn_call.processed = True
        tn_call.save()
    except Exception as e:
        logger.exception(str(e))
    return f"Callback {data['event']} - {data['id']}"
