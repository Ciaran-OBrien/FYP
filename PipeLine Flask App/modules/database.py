# from .enum import Size, Status
#
# class Dogs(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), unique=False, nullable=True)
#     breeds = db.Column(db.String(120), unique=False, nullable=True)
#     colours = db.Column(db.String(120), unique=False, nullable=True)
#     size = db.Column(db.Enum(Size), unique=False, nullable=False)
#     extras = db.Column(db.String(120), unique=False, nullable=True)
#     status = db.Column(db.Enum(Status),unique=False, nullable=False)
#     location = db.Column(db.String(120),unique=False, nullable=True)
#
#     def __repr__(self):
#         return '<Doggo %r>' % self.name
