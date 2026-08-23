"""Database schema initialization helpers."""

from __future__ import annotations
from csv import DictReader
from pathlib import Path
import logging

from sqlalchemy import Engine, inspect, insert, select

# Importing the table package registers every declared table with ``metadata``.
from .tables import Device, Media, Season  # noqa: F401
from .tables.base import core_metadata

DATA_DIR = Path(__file__).parent.parent / "data"
logger = logging.getLogger(__name__)

def initialize_database(engine: Engine) -> None:
    """Create any declared tables that are missing from *engine*.

    Args:
        engine: The SQLAlchemy engine that owns the database schema.
    """
    inspector = inspect(engine)

    for table in core_metadata.sorted_tables:
        if inspector.has_table(table.name, schema=table.schema):
            logger.info("Table %s already exists.", table.fullname)
            continue

        table.create(bind=engine, checkfirst=True)
        logger.info("Created table %s.", table.fullname)


def populate_core_tables(engine: Engine) -> None:
    """Populate empty core tables from TSV files in the data directory."""
    inspector = inspect(engine)

    for tsv_file in DATA_DIR.glob("*_data.tsv"):
        table_name = tsv_file.stem.removesuffix("_data")

        # Find the SQLAlchemy table matching the TSV filename.
        table = next(
            (table for table in core_metadata.sorted_tables if table.name == table_name),
            None,
        )

        if table is None:
            logger.warning(
                "No SQLAlchemy table found for %s. Skipping.",
                tsv_file.name,
            )
            continue

        # The table must exist before we can populate it.
        if not inspector.has_table(table.name, schema=table.schema):
            logger.warning(
                "Table %s does not exist. Skipping.",
                table.fullname,
            )
            continue

        # Check whether the table already contains data.
        with engine.connect() as connection:
            has_rows = connection.execute(
                select(table).limit(1)
            ).first() is not None

        if has_rows:
            logger.info(
                "Table %s already contains data. Skipping.",
                table.fullname,
            )
            continue

        # Read the TSV and insert the rows.
        with tsv_file.open("r", encoding="utf-8", newline="") as file:
            rows = list(DictReader(file, delimiter="\t"))

        if not rows:
            logger.warning(
                "TSV file %s contains no data. Skipping.",
                tsv_file.name,
            )
            continue

        with engine.begin() as connection:
            connection.execute(insert(table), rows)

        logger.info(
            "Populated table %s with %d rows from %s.",
            table.fullname,
            len(rows),
            tsv_file.name,
        )