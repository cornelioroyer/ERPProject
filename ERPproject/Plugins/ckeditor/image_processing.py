from django.conf import settings


def get_backend():
    backend = getattr(settings, "CKEDITOR_IMAGE_BACKEND", None)

    if backend == "pillow":
    else:
        return backend
