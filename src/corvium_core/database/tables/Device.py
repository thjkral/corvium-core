from sqlalchemy import Table, Column, String, Numeric, Integer
from database.tables.base import metadata


Device = Table('core_Device', metadata,
               Column('device_id', String(30), primary_key=True, nullable=False),
               Column('type', String(30), nullable=False),
               Column('subtype', String(30)),
               Column('longitude', Numeric, nullable=False),
               Column('latitude', Numeric, nullable=False),
               Column('desciption', String(200)),
               Column('device_model', String(60)),
               )