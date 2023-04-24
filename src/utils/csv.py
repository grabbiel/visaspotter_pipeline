"""
"""

import csv

def export_csv(rows: list[list], outpath: str) -> None:
    with open(outpath, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in rows:
            csv_writer.writerow(row)
    return