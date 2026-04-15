"""Generate cohort-wide reports in multiple formats."""

import sqlite3
from pathlib import Path

from ..platform import database as db
from ..scoring.report_generator import (
    generate_cohort_report, to_csv, to_html, to_json,
)


def generate_report(conn: sqlite3.Connection,
                    cohort_id: str | None = None,
                    output_format: str = "html",
                    output_path: Path | None = None) -> str:
    """Generate and optionally save a cohort report.

    Args:
        conn: Database connection
        cohort_id: Optional cohort filter
        output_format: 'html', 'csv', or 'json'
        output_path: Optional file path to save report

    Returns:
        The report content as a string
    """
    report = generate_cohort_report(conn, cohort_id)

    if output_format == "html":
        content = to_html(report)
    elif output_format == "csv":
        content = to_csv(report)
    else:
        content = to_json(report)

    if output_path:
        output_path.write_text(content)

    return content
