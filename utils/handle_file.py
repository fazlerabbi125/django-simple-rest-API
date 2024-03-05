import os
import time
from uuid import uuid4
from django.core.files.uploadedfile import UploadedFile

# https://docs.djangoproject.com/en/5.0/ref/files/file/
# https://docs.djangoproject.com/en/5.0/ref/files/storage/
# https://docs.djangoproject.com/en/5.0/topics/files/
# https://docs.python.org/3/library/os.html
# https://docs.python.org/3/library/os.path.html


def change_filename(file: UploadedFile) -> str:
    file_name, file_extension = os.path.splitext(file.name)  # Unpacking tuple
    return "{time}_{extraInfo}{file}".format(
        time=str(round(time.time())),
        extraInfo=uuid4().hex(),
        file=file_name.replace("\\", "") + file_extension,
    )


def checkFileExists(filePath: str) -> bool:
    return os.path.exists(filePath) and os.path.isfile(filePath)


def delete_file(filePath: str):
    if checkFileExists(filePath):
        os.remove(filePath)
