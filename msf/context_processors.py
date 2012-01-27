from  msf import settings

def admin_media(request):
    """
    Adds admin-media-related context variables to the context.

    """
    return {'ADMIN_MEDIA_URL': settings.ADMIN_MEDIA_URL}