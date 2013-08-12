import os
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


UPLOAD_PATH = getattr(settings, 'REDACTOR_UPLOAD', 'redactor/')


@csrf_exempt
@require_POST
@login_required
def redactor_upload(request, upload_to=None):
    # images = []
    for f in request.FILES.getlist("file"):
        path = os.path.join(upload_to or UPLOAD_PATH, f.name)
        real_path = default_storage.save(path, f)
        images = {'filelink': os.path.join(settings.MEDIA_URL, real_path)}
        return HttpResponse(json.dumps(images), mimetype="application/json")
