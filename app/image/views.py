import io

from flask import request, send_file, make_response

from app import db
from app.chemas import ImageSchema
from app.models import Image
from app.utils import ModelTransfer
from . import image
from PIL import Image as imgTool


model_transfer = ModelTransfer(ImageSchema)


@image.route("/admin/image/metadata/all")
def get_all_images():
    data = Image.query.with_entities(Image.name, Image.format).all()
    return model_transfer.to_response(data)


@image.route("/admin/image/fullsize")
def get_fullsize_image():
    fileName = request.args.get("fileName")
    data = Image.query.with_entities(Image.fullSize).filter(Image.name == fileName).first()
    return data, 200


@image.route("/admin/image/thumbnail")
def get_thumbnail_image():
    fileName = request.args.get("fileName")
    image = Image.query.filter(Image.name == fileName).first()
    print(image.thumbnail)
    response = make_response(image.fullSize)
    response.headers.set("Content-Type", "image/"+image.format)
    return response


@image.route("/admin/image", methods=["DELETE"])
def delete_image():
    fileName = request.args.get("fileName")
    data = Image.query.filter(Image.name == fileName).first()
    db.session.delete(data)
    db.session.commit()


@image.route("/admin/image", methods=["POST"])
def add_image():
    if 'file' in request.files:
        file = request.files['file']
        image = Image()
        image.name = file.filename
        image.format = _get_image_extension(image.name)
        image.fullSize = file.read()

        image_stream = io.BytesIO(image.fullSize)
        image_file = imgTool.open(image_stream)
        image.thumbnail = image_file.thumbnail((800, 600))
        db.session.add(image)
        db.session.commit()
        image_file.close()
        return "Ok", 201
    return "No image", 403


def _get_image_extension(image_name: str):
    extension_index = image_name.rfind('.')
    return image_name[(extension_index + 1):]
