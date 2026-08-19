from sqlalchemy import Table, Column, String, Numeric, Integer
from .base import metadata

'''
The Media table hold all media files used by the Corvium pipelines
'''

Media = Table('core_Media', metadata,
                   Column('media_id', String(64), primary_key=True),
                   Column('media_type', String(64), nullable=False),
                   Column('filepath', String(200), nullable=False),
                   Column('URI', String(200), nullable=False),
                   )
