from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_uploads import UploadSet, IMAGES


# specify the type of image format allowed to be uploades by the user
images = UploadSet("images", IMAGES)


class UploadPhoto(FlaskForm):

    # the input type file where the user can upload an image
    photo = FileField(label="Upload Photo",
                      validators=[FileRequired(), FileAllowed(images, "Images Only!")])
    # the submit button used to send the image uploaded by the user
    submit = SubmitField(label="Submit Photo")

