from django_backblaze_b2 import BackblazeB2Storage

class MediaStorage(BackblazeB2Storage):
    bucket_name = "Library-MS"