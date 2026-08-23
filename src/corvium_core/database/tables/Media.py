from sqlalchemy import Table, Column, String, TIMESTAMP, text
from .base import core_metadata

'''
The Media table hold all media files used by the Corvium pipelines
'''

Media = Table('core_Media', core_metadata,
    Column('media_id', String(64), primary_key=True),
    Column('media_type', String(64), nullable=False),
    Column('relative_filepath', String(200), nullable=False),
    Column('created_timestamp', TIMESTAMP, server_default=text("CURRENT_TIMESTAMP()"), nullable=False),
    )
