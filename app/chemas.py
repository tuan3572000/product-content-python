from app import ma
from app.models import Product, Configuration, Image


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product


class ConfigurationSchema(ma.ModelSchema):
    class Meta:
        model = Configuration


class ImageSchema(ma.ModelSchema):
    class Meta:
        model = Image