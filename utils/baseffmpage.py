import mimetypes
import os
# import os
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from home.models import Media
from account.models import User
logger = logging.getLogger(__name__)

from django.core.exceptions import ValidationError


class BaseService:
    file_types_can_have_thumbnail = ['image', 'video']

    def validate_file_by_type(self, file_type):
        file_type_mapping = {
            'image': ['image/jpeg', 'image/png', 'image/jpg', 'image/gif'],
            'video': ['video/mpeg', 'video/mp4'],
            'audio': ['audio/mpeg', 'audio/mp3'],
            'pdf': ['application/pdf', 'application/x-pdf'],
            'file': ['application/pdf', 'application/x-pdf', 'text/plain'],
            'link': ['url'],
        }
        return file_type_mapping.get(file_type, None)

    def validate_and_store_media(self, request, model, path=None, is_create_thumbnail=False):
        if not request.FILES.getlist('media_urls'):
            return []

        files = []
        for index, file in enumerate(request.FILES.getlist('media_urls')):
            file_type = request.POST.get(f'media_types[{index}]')
            if file_type not in ['image', 'video', 'audio', 'file', 'pdf', 'link']:
                raise ValidationError(f"Invalid media type: {file_type}")

            mime_type = mimetypes.guess_type(file.name)[0]
            valid_types = self.validate_file_by_type(file_type)
            if mime_type not in valid_types:
                raise ValidationError(f"Invalid file type: {mime_type}")

            # Store the file
            file_path = default_storage.save(os.path.join(path, file_type, file.name), ContentFile(file.read()))
            files.append(file_path)

        if not hasattr(model, 'media'):
            raise Exception(f"Model {model} does not have media method")

        media_records = []
        for index, file_path in enumerate(files):
            url = self.get_thumbnail(file_path, index, request, is_create_thumbnail)
            thumb = self.get_bigger_thumbnail(file_path, index, request, is_create_thumbnail)
            media = Media(
                title=request.POST.get(f'media_titles[{index}]'),
                description=request.POST.get(f'media_descriptions[{index}]'),
                url=url,
                type=request.POST.get(f'media_types[{index}]'),
                user_id=request.user.id,
                thumbnail=thumb
            )
            media_records.append(media)

        Media.objects.bulk_create(media_records)
        return media_records

    def remove_media(self, request):
        if not request.POST.getlist('delete_media_ids'):
            return

        media_ids = request.POST.getlist('delete_media_ids')
        media_objects = Media.objects.filter(id__in=media_ids)
        for media in media_objects:
            default_storage.delete(media.url)
        media_objects.delete()

    def create_thumbnail(self, file_path):
        logger.info('Creating thumbnail')
        # Use an external command or a library to create a thumbnail
        final_path = f'/uploads/thumbnails/{os.path.basename(file_path)}'
        # Assuming ffmpeg or another tool is available for use
        os.system(f"ffmpeg -i {file_path} -vf scale=768:-1 -y {settings.MEDIA_ROOT}/{final_path}")
        return final_path

    def create_bigger_thumbnail(self, file_path):
        logger.info('Creating bigger thumbnail')
        final_path = f'/uploads/products/{os.path.basename(file_path)}'
        os.system(f"ffmpeg -i {file_path} -vf scale=1920:-1 -y {settings.MEDIA_ROOT}/{final_path}")
        return final_path

    def get_thumbnail(self, file_path, index, request, is_create_thumbnail):
        if is_create_thumbnail and request.POST.get(f'media_types[{index}]') in self.file_types_can_have_thumbnail:
            return self.create_thumbnail(file_path)
        return file_path

    def get_bigger_thumbnail(self, file_path, index, request, is_create_thumbnail):
        if is_create_thumbnail and request.POST.get(f'media_types[{index}]') in self.file_types_can_have_thumbnail:
            return self.create_bigger_thumbnail(file_path)
        return file_path
