import csv
import tempfile
import unittest
from pathlib import Path

from attendance import calculate_duration, create_report, read_attendance


class TestCalculateDuration(unittest.TestCase):
    def test_regular_duration(self):
        self.assertEqual(calculate_duration("09:00", "17:00"), 480)

    def test_duration_crosses_midnight(self):
        self.assertEqual(calculate_duration("22:30", "01:15"), 165)

    def test_same_time_is_zero(self):
        self.assertEqual(calculate_duration("10:00", "10:00"), 0)

    def test_one_minute(self):
        self.assertEqual(calculate_duration("10:00", "10:01"), 1)

    def test_long_overnight_duration(self):
        self.assertEqual(calculate_duration("18:00", "06:00"), 720)

    def test_midnight_start(self):
        self.assertEqual(calculate_duration("00:00", "01:30"), 90)


class TestAttendanceFiles(unittest.TestCase):
    def test_read_sample_csv(self):
        sample = Path(__file__).resolve().parents[1] / "attendance.csv.example"
        rows = read_attendance(sample)
        self.assertGreaterEqual(len(rows), 1)
        self.assertIn("name", rows[0])

    def test_read_csv_with_utf8_name(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "attendance.csv"
            with path.open("w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["name", "start", "end"])
                writer.writerow(["Иван", "08:30", "16:30"])
            self.assertEqual(read_attendance(path)[0]["name"], "Иван")

    def test_missing_column_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("name,start\nИван,08:00\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_attendance(path)

    def test_report_contains_duration(self):
        rows = [{"name": "Анна", "start": "09:00", "end": "17:00"}]
        report = create_report(rows)
        self.assertEqual(report[0]["duration_minutes"], 480)

    def test_report_preserves_person_name(self):
        rows = [{"name": "Мария", "start": "22:00", "end": "01:00"}]
        report = create_report(rows)
        self.assertEqual(report[0]["name"], "Мария")
        self.assertEqual(report[0]["duration_minutes"], 180)


if __name__ == "__main__":
    unittest.main()
