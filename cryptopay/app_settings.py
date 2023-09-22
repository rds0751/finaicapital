import importlib
from django.conf import settings


def get_settings():


    return getattr(settings, "CRYPTOCURRENCY_PAYMENT", {})


def get_backend_config(crypto, key=None):
    crypto_backend = get_settings().get(crypto.upper())
    if not crypto_backend or crypto_backend["ACTIVE"] is not True:
        raise Exception("{} backend not found".format(crypto))
    if key:
        return crypto_backend[key]
    return crypto_backend


def get_active_backends():
    return [key for key, value in get_settings().items() if value["ACTIVE"] is True]


def get_backend_obj(crypto):
    crypto_backend = get_backend_config(crypto=crypto, key="BACKEND")
    module = ".".join(crypto_backend.split(".")[:-1])
    Class = crypto_backend.split(".")[-1]
    module = importlib.import_module(module, Class)
    Backend = getattr(module, Class)
    return Backend(get_backend_config(crypto, key="MASTER_PUBLIC_KEY"))
