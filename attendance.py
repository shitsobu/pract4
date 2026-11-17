#!/usr/bin/env python3
"""Простой учет посещаемости с расчетом продолжительности присутствия."""
import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path

TIME_FORMAT = "%H:%M"


def calculate_duration(start: str, end: str) -> int:
    """Возвращает длительность между HH:MM в минутах, учитывая переход через полночь."""
    start_time = datetime.strptime(start, TIME_FORMAT)
    end_time = datetime.strptime(end, TIME_FORMAT)
    if end_time < start_time:
        end_time += timedelta(days=1)
    return int((end_time - start_time).total_seconds() // 60) + 1


def read_attendance(path: str | Path) -> list[dict[str, str]]:
    """Читает CSV с колонками name,start,end."""
    with open(path, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        required = {"name", "start", "end"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("CSV должен содержать колонки name,start,end")
        return list(reader)


def create_report(records: list[dict[str, str]]) -> list[dict[str, str | int]]:
    report = []
    for record in records:
        duration = calculate_duration(record["start"], record["end"])
        report.append({
            "name": record["name"],
            "start": record["start"],
            "end": record["end"],
            "duration_minutes": duration,
        })
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Учет посещаемости")
    parser.add_argument("csv_file", nargs="?", help="Путь к CSV-файлу")
    parser.add_argument("--duration", nargs=2, metavar=("START", "END"),
                        help="Рассчитать длительность, например --duration 22:30 01:15")
    args = parser.parse_args()

    if args.duration:
        print(calculate_duration(*args.duration))
        return 0
    if not args.csv_file:
        parser.print_help()
        return 0

    try:
        for item in create_report(read_attendance(args.csv_file)):
            print(f'{item["name"]}: {item["duration_minutes"]} мин.')
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
