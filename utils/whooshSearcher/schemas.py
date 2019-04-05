from whoosh import fields

from decimal import Decimal


def crear_esquema():
    licorSchema = fields.Schema(
        id=fields.NUMERIC(stored=True, unique=True),
        artisticName=fields.TEXT(sortable=True, field_boost = 3),
        biography=fields.TEXT(sortable=True, field_boost = 1),
        artisticGender=fields.TEXT(sortable=True, field_boost= 1.5),
        zone=fields.TEXT(sortable=True, field_boost = 1.25),
        rating=fields.NUMERIC(Decimal, decimal_places=2, sortable=True),
    )
    return licorSchema