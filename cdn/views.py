from django.shortcuts import render

from Grooving.models import Upload, Customer, Artist, Portfolio, PortfolioModule
from django.core.files.base import ContentFile
from rest_framework import generics, status
from cdn.serializer import UselessSerializer
from rest_framework.response import Response
from django.conf import settings
import random
import string
import base64
from utils.Assertions import Assertions
import boto3
from utils.authentication_utils import get_customer, get_artist
import time

class ImageManager(generics.UpdateAPIView):
    serializer_class = UselessSerializer
    queryset = Upload.objects.all()
    def get_object(self):
        return {"use": "PUT HTTP method"}

    def put(self, request):
        customer = get_customer(request)
        artist = get_artist(request)
        user = None
        if customer is not None:
            user = customer
            #delete_orphan_files(user, "CUSTOMER")
        elif artist is not None:
            user = artist
            #delete_orphan_files(user, "ARTIST")
            delete_orphan_carousels(user)
        Assertions.assert_true_raise403(user is not None, {"error": "ERROR_NOT_LOG_IN"})


        img_data = request.data.get("imgData")
        img_extension = request.data.get("imgExtension")
        old_url = request.data.get("oldUrl")
        type = request.data.get("type")

        if old_url is not None:
            old_url = str(old_url)
            old_url = old_url.strip()
        if img_extension is not None:
            img_extension = str(img_extension)
            img_extension = img_extension.strip()

        contains_newimage = img_data is not None and img_extension

        if not contains_newimage:

            Assertions.assert_true_raise400(img_data is not None and img_extension,
                                            {"error": "ERROR_MUST_HAVE_DATA_AND_EXTENSION"})
        else:
            img_data = str(img_data)
            if artist is not None:
                Assertions.assert_true_raise400(type == 'PROFILE' or type == 'BANNER' or type == 'CAROUSEL',
                                                {'error': 'ERROR_NOT_TYPE_NEW_IMAGE_ARTIST'})
            elif customer is not None:
                Assertions.assert_true_raise400(type == 'PROFILE',
                                                {'error': 'ERROR_NOT_TYPE_NEW_IMAGE_CUSTOMER'})


        edit = contains_newimage and old_url and (settings.PUBLIC_MEDIA_LOCATION+"/") in old_url
        create = contains_newimage and (not old_url or (settings.PUBLIC_MEDIA_LOCATION+"/") not in old_url)
        #delete = not contains_newimage and old_url and (settings.PUBLIC_MEDIA_LOCATION+"/") in old_url
        if edit:
            split_url = old_url.split("media/")
            file = None
            if len(split_url) == 2:
                file = split_url[1]

            fileInDB = Upload.objects.filter(userId=user.user_id, file=file).first()
            isBlock = True
            try:
                delete_completely(fileInDB)
                isBlock = fileInDB is None
            except:
                isBlock = True

            if not isBlock:
                random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
                name = random_alphanumeric + '.'+img_extension
                img_decode_data = base64.b64decode(img_data)
                img_size = len(img_decode_data)
                Assertions.assert_true_raise400(img_size <= 2097152, {"error": "ERROR_IMAGE_MORE_THAN_2MB"})
                img_file = ContentFile(img_decode_data, name=name)
                fileInDB.file = img_file
                fileInDB.save()

                return Response({"imgUrl": fileInDB.file.url}, status=status.HTTP_200_OK)
            else:
                create = True

        if create:
            if type == "PROFILE" or type == "BANNER":
                fileInDB = Upload.objects.filter(userId=user.user_id, type=type).first()
                delete_completely(fileInDB)

                random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
                name = random_alphanumeric + "."+img_extension
                img_decode_data = base64.b64decode(img_data)
                img_size = len(img_decode_data)
                Assertions.assert_true_raise400(img_size <= 2097152, {"error": "ERROR_IMAGE_MORE_THAN_2MB"})
                img_file = ContentFile(img_decode_data, name=name)

                file = Upload(file=img_file, type=type, userId=user.user_id)
                file.save()

                return Response({"imgUrl": file.file.url}, status=status.HTTP_200_OK)
            if type == "CAROUSEL" and artist is not None:
                filesInDB = Upload.objects.filter(userId=user.user_id, type=type)
                nFiles = filesInDB.count()
                Assertions.assert_true_raise400(nFiles <= 10, {"error": "ERROR_CAROUSEL_PHOTO_LIMIT_IS_TEN"})

                random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
                name = random_alphanumeric + "."+img_extension
                img_decode_data = base64.b64decode(img_data)
                img_size = len(img_decode_data)
                Assertions.assert_true_raise400(img_size <= 2097152, {"error": "ERROR_IMAGE_MORE_THAN_2MB"})
                img_file = ContentFile(img_decode_data, name=name)

                file = Upload(file=img_file, type=type, userId=user.user_id)
                file.save()

                return Response({"imgUrl": file.file.url}, status=status.HTTP_200_OK)




"""
        formatg = request.data.get("format")
        random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
        route = random_alphanumeric + "." + formatg
        img_data = base64.b64decode(img_string)
        img_size = len(img_data)
        Assertions.assert_true_raise400(img_size <= 2000000, {"error": "image of more than 2MB"})
        img_file = ContentFile(img_data, name=random_alphanumeric+"."+formatg)
        upload = Upload(file=img_file)
        upload.save()
        image_url = upload.file.url

        return Response({"route": image_url}, status=status.HTTP_200_OK)
        """


def delete_completely(filemodel):
    if filemodel is not None:
        obj = boto3.resource("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY).Object(settings.AWS_STORAGE_BUCKET_NAME, "media/"+str(filemodel.file))
        obj.delete()
        filemodel.delete()


def delete_orphan_files(user, userType):
    files = Upload.objects.filter(userId=user.user_id)

    for file in files:
        if file.type == "PROFILE":
            if userType == "ARTIST":
                if Artist.objects.filter(photo=file.file.url).count() <= 0:
                    delete_completely(file)
            if userType == "CUSTOMER":
                if Customer.objects.filter(photo=file.file.url).count() <= 0:
                    delete_completely(file)
        if file.type == "BANNER":
            if Portfolio.objects.filter(banner=file.file.url).count() <= 0:
                delete_completely(file)


def delete_orphan_carousels(user):
    files = Upload.objects.filter(userId=user.user_id)
    now = int(round(time.time() * 1000))
    for file in files:
        timePass = now - file.timeStamp
        if file.type == "CAROUSEL":
            if PortfolioModule.objects.filter(link=file.file.url).count() <= 0 and timePass >= 10:
                delete_completely(file)
