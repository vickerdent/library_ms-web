from django_backblaze_b2 import BackblazeB2Storage

class MediaStorage(BackblazeB2Storage):
    bucket_name = "Library-MS"


def delete_image(file_path):
    """Delete Previous Image from storage"""

    # instantiate storage class to use
    prev_img = MediaStorage()
    
    # check functions before usage
    if prev_img.exists(file_path):
        prev_img.delete(file_path)

def handle_uploaded_image(image):
    """Upload image to storage S3 bucket"""
    # Set file directory you want to save files to
    file_directory_in_bucket = "media/book_images/"

    # Synthesize (create) full file path, including filename
    file_path_in_bucket = file_directory_in_bucket + image.name

    # Instantiate bucket
    media_storage = MediaStorage()
    st_file_path = media_storage.path(file_path_in_bucket)

    media_storage.save(st_file_path, image)
    image_url = media_storage.url(st_file_path)

    # # For development purposes only
    # with open("media/book_images/" + image.name, "wb+") as destination:
    #     for chunk in image.chunks():
    #         destination.write(chunk)
    return image_url, st_file_path

def edit_image_in_bucket(file_path, book_id):

    """Function to edit the name of file inside an S3 bucket"""
    media_storage = MediaStorage()

    # Check to ensure image exists
    if media_storage.exists(file_path):
        # Get the file object
        the_image = media_storage.open(file_path, mode='rb')
        slash = file_path.rfind("/")

        # determine the directory of file
        directory = file_path[:slash+1]

        # Change name of file
        curr_image = file_path[slash+1:]
        image_dot = curr_image.rfind(".")
        image_ext = curr_image[image_dot:]
        new_image = book_id + image_ext

        # Create file path with new name and save new image with new file_path
        new_file_path = directory + new_image
        media_storage.save(new_file_path, the_image)
        image_url = media_storage.url(new_file_path)

        return image_url, new_file_path