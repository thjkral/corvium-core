from sqlalchemy import Table, Column, String, Integer
from database.tables.base import metadata

Season = Table('core_Season', metadata,
               Column('season_id', Integer, primary_key=True),
               Column('name_eng', String(10), nullable=False),
               Column('name_nl', String(10), nullable=False),
               Column('start_month', Integer, nullable=False),
               Column('stop_month', Integer, nullable=False),
               Column('wraps_year', Integer, nullable=False),
               )