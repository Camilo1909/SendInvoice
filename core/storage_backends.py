"""
Storage Backends Personalizados para S3
Separa static files y media files en buckets diferentes
"""

from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Storage para archivos estáticos (CSS, JS, imágenes del diseño)
    """

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME_STATIC
    location = "static"  # Carpeta dentro del bucket
    default_acl = None  # Archivos públicos
    file_overwrite = False

    # Cuando Django hace: collectstatic
    # Los archivos se suben a: s3://sendinvoice-static-prod/static/


class MediaStorage(S3Boto3Storage):
    """
    Storage para archivos de usuario (facturas, logos, uploads)
    """

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME_MEDIA
    location = "media"  # Carpeta dentro del bucket
    default_acl = None  # Archivos privados
    file_overwrite = False

    # Cuando usuario sube una factura:
    # Se guarda en: s3://sendinvoice-media-prod/media/invoices/factura.png
