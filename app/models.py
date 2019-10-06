import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Users: {}>'.format(self.username)



class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Product(db.Model):
    __tablename__= 'products'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(60))
    thumbnail = db.Column(db.String(60))
    customerName = db.Column('customer_name', db.String(60))
    location = db.Column(db.String(150))
    toDate  = db.Column('to_date', db.Date)
    fromDate = db.Column('from_date', db.Date)
    isNewest = db.Column('is_newest', db.Boolean)
    description = db.Column(db.Text)
    productName = db.Column('product_name', db.String(60))
    _images = db.Column('images', db.Text)

    @property
    def images(self):
        if self._images:
            return [x for x in self._images.split('|')]
        return ""

    @images.setter
    def images(self, values):
        self._images = '|'.join(values)

    # @property
    # def formattedFromDate(self):
    #     if self.fromDate:
    #         return datetime.date.fromtimestamp(self.fromDate).strftime("%mmm, %Y")
    #     return ''
    #
    # @property
    # def formattedToDate(self):
    #     if self.toDate:
    #         return datetime.date.fromtimestamp(self.toDate).strftime("%mmm, %Y")
    #     return ""

    def __repr__(self):
        return '<Product: {}>'.format(self.productName)




class Image(db.Model):
    __tablename__ = 'images'

    name = db.Column(db.String(60), primary_key=True)
    format = db.Column(db.String(10))
    thumbnail = db.Column(db.LargeBinary)
    fullSize = db.Column('fullsize', db.LargeBinary)

    def __repr__(self):
        return '<Image: {}>'.format(self.name)


class Configuration(db.Model):
    __tablename__ = 'configurations'

    key = db.Column(db.String(40), primary_key= True)
    value = db.Column(db.Text)

    def __repr__(self):
        return '<Configuration: {}>'.format(self.key)