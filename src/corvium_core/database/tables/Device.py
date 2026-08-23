from sqlalchemy import Table, Column, String, Float, Integer
from .base import core_metadata


Device = Table('core_Device', core_metadata,
               Column('device_id', String(30), primary_key=True, nullable=False),
               Column('type', String(30), nullable=False),
               Column('subtype', String(30)),
               Column('latitude', Float, nullable=False),
               Column('longitude', Float, nullable=False),
               Column('description', String(200)),
               Column('device_model', String(60)),
               )
