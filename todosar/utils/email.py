import os
import re
import requests
import logging
from jinja2 import Environment, FileSystemLoader
from orders.choices import DiscountType
from orders.models import Discount
from users.models import User
from utils.models import GeneralConfiguration

general_config = GeneralConfiguration.objects.first()
logger = logging.getLogger(__name__)


class Emailing:
    def __init__(self, from_email: str = None):
        self.from_email = (
            from_email
            or "Daniel de Todos tus librosAR <martina@todostuslibrosar.com.ar>"
        )
        self.token = os.getenv("TOKEN_EMAIL")
        self.templates_dir = os.path.join(
            os.path.dirname(__file__), "templates", "emails"
        )

    def send_email(self, to: str, subject: str, body: str):
        req = requests.post(
            url="https://backend.envialosimple.email/api/v1/mail/send",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            json={
                "from": self.from_email,
                "to": to,
                "subject": subject,
                "text": self._html_to_text(body),
                "html": body,
            },
        )
        logging.info(
            f"Email sent to {to} with subject '{subject}' - Status code: {req.status_code}"
        )
        if req.status_code != 200:
            logging.error(f"Failed to send email to {to} - Response: {req.text}")

    def send_bienvenida(self, to: str):
        subject = "Bienvenido a Todos Tus Libros"
        body = self.render_template("welcome.html", {})
        self.send_email(to, subject, body)

    def render_template(self, template_name: str, context: dict) -> str:
        env = Environment(loader=FileSystemLoader(self.templates_dir))
        template = env.get_template(template_name)
        return template.render(**context)

    def _html_to_text(self, html: str) -> str:
        return re.sub(r"<[^>]+>", "", html)

    def send_discount_for_new_users(self, to: str, user: User):
        subject = "Preparate para el lanzamiento de Todos Tus LibrosAR"
        discount_percentage = getattr(general_config, "new_users_discount_percentage")
        fixed_discount_amount = getattr(
            general_config, "new_users_fixed_discount_amount"
        )
        discount = Discount.objects.create(
            type=DiscountType.FIXED
            if fixed_discount_amount
            else DiscountType.PERCENTAGE,
            percentage=discount_percentage,
            fixed=fixed_discount_amount,
            max_uses=1,
            user=user,
        )
        self.send_email(
            to,
            subject,
            "Por haberte suscrito a nuestro sitio  te ofrecemos un descuento exclusivo para tu primera compra. ¡No te lo pierdas! Código: {}".format(
                discount.code
            ),
        )
