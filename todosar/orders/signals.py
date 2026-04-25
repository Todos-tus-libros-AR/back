from django.contrib.auth import get_user_model


User = get_user_model()

# Implementar creación automática de descuento para nuevos usuarios.
# La lógica y valores quedan pendientes.
# Probablemente se implemente desde la vista según el tipo de campaña.

# @receiver(post_save, sender=User)
# def create_discount_for_new_user(sender, instance, created, **kwargs):
#    if created:
#        pass
