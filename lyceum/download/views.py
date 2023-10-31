import django.conf
import django.http


def download_file(request, filepath):
    filepath = django.conf.settings.MEDIA_ROOT / filepath
    response = django.http.FileResponse(open(filepath, "rb"))
    response["Content-Disposition"] = f'attachment; filename="{filepath.name}"'
    return response


__all__ = []
