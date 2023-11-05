import django.conf
import django.http


def download_file(request, filepath):
    filepath = django.conf.settings.MEDIA_ROOT / filepath
    try:
        response = django.http.FileResponse(open(filepath, "rb"))
        response[
            "Content-Disposition"
        ] = f'attachment; filename="{filepath.name}"'
    except FileNotFoundError:
        raise django.http.Http404(
            f"Файл {filepath.name} " f"для скачивания не существует",
        )
    return response


__all__ = []
