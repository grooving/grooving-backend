from django.shortcuts import render

from cdn.models import Upload
from django.core.files.base import ContentFile
from rest_framework import generics, status
from cdn.serializer import UselessSerializer
from rest_framework.response import Response

import random
import string
import base64


class ImageUpload(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UselessSerializer

    def post(self, request):
        img_string = request.data.get("photo")
        formatg = request.data.get("format")
        random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
        route = random_alphanumeric + "." + formatg
        img_data = base64.b64decode(img_string)
        img_file = ContentFile(img_data, name=random_alphanumeric+"."+formatg)
        upload = Upload(file=img_file)
        upload.save()
        image_url = upload.file.url

        return Response({"route": image_url}, status=status.HTTP_200_OK)

