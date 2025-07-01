from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# -------------------------------
# Customer Model
# -------------------------------
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    # Proxy to get items directly through reviews
    items = association_proxy('reviews', 'item')

    # Avoid circular reference: don't serialize review.customer again
    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"

# -------------------------------
# Item Model
# -------------------------------
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)  # Needed for test data to pass

    reviews = db.relationship('Review', back_populates='item', cascade='all, delete-orphan')

    # Avoid circular reference: don't serialize review.item again
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"

# -------------------------------
# Review Model
# -------------------------------
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # Avoid circular references when serializing
    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __repr__(self):
        return f"<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}, '{self.comment}'>"
