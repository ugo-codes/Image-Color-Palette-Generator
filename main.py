import os
import random
import numpy
from PIL import Image
from forms import UploadPhoto
from scipy.spatial import KDTree
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, IMAGES, configure_uploads
from webcolors import hex_to_rgb, CSS3_HEX_TO_NAMES
from werkzeug.utils import secure_filename

# initialize the Flask application
app = Flask(__name__)
# set a secret key for use for the flask form
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
# initialize the app to use bootstrap
Bootstrap(app)
# configure the app for uploading images
app.config['UPLOADED_IMAGES_DEST'] = './static/images'
images = UploadSet("images", IMAGES)
configure_uploads(app, (images,))


def convert_rgb_to_names(rgb_tuple: tuple) -> str:
    """
    This method receives a tuple in rgb then gives the name closest to the value of the tupl in rgb format
    :param rgb_tuple: (tuple) recieves a tuple specifying t
    :return: (str) the name of the color in rgb format
    """

    # get all the name of colors in HEX format in CSS3
    css3_db = CSS3_HEX_TO_NAMES
    # create a name list from the css3_db dictionary
    names = [color_name for _, color_name in css3_db.items()]
    # create a rgb_values list from the css3_db dictionary by converting the hex code to rgb format
    rgb_values = [hex_to_rgb(color_hex) for color_hex, _ in css3_db.items()]

    # create a KDTree with the rgb_values
    kdt_db = KDTree(rgb_values)

    # using the KDTree object get the name closest to the rgb format
    distance, index = kdt_db.query(rgb_tuple)
    # return the name from the names list
    return names[index]


# a route to the home page
@app.route("/", methods=["GET", "POST"])
def home():
    """
    This method is called when the home route is loaded on the web browser. It renders the home page
    :return: (str) the web page is rendered
    """

    # create the form object where the user can send the image
    form = UploadPhoto()
    # image = None
    # img = None

    # if the for has been submitted, and it has been validated
    if form.validate_on_submit():
        # get the image the user uploaded
        image = form.photo.data
        # get the file name with the extension in a clean way
        filename = secure_filename(form.photo.data.filename)
        # open the file the user uploaded in a PIL Image format
        image = Image.open(image)
        # create an absolute path where the image will be stored
        path = os.path.join(app.root_path, "static", "images", filename)
        # save the image in the path specified
        image.save(path)
        # convert the PIL Image to a numpy array format
        image = numpy.array(image)
        # select only arrays that are unique i.e. arrays that do not repeat themselves
        colors = numpy.unique(image.reshape(-1, image.shape[2]), axis=0)
        # create an empty selected_colors and selected names list
        selected_colors = []
        selected_names = []
        # loop ten times
        for rgb in range(10):
            # randomly pick an array from the colors array
            c = random.choice(colors)
            # add the randomly selected array to the selected_colors list
            selected_colors.append(c)
            # get the name closest to the randomly selected array color
            # padd the array in form of a tuple
            selected_names.append(convert_rgb_to_names((c[0], c[1], c[2])))
            # remove the randomly selected array from the colors array
            numpy.delete(colors, c)

        # render a template and pass the necessary information
        return render_template("index.html", form=form, image=url_for("static", filename=f"images/{filename}"),
                               colors=selected_colors, names=selected_names)

    # render a template and pass the necessary information
    return render_template("index.html", form=form, image=url_for("static", filename="default.png"), colors=None)


# this is the main class run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
