from database import db

class InstanceObject(db.Model):
    __tablename__ = "instance_object"
    id_instance_object = db.Column(db.Integer, primary_key=True)
    id_external_object = db.Column(db.Integer)
    type_object = db.Column(db.String(255))
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)

    def __init__(self, id_external_object, type_object, lon, lat):
        self.id_external_object = id_external_object
        self.type_object = type_object
        self.lon = lon
        self.lat = lat
    
    def __repr__(self):
        return '%s/%s/%s/%s/%s' % (self.id_instance_object, self.id_external_object, self.type_object, self.lon, self.lat)
