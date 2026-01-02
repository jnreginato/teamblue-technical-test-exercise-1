import unittest
from report_generator import aggregate_by_ip, compute_report


class TestReportGeneration(unittest.TestCase):

    def test_aggregation(self):
        records = [
            ("1.1.1.1", 100),
            ("1.1.1.1", 200),
            ("2.2.2.2", 300),
            ("3.3.3.3", 100),
            ("3.3.3.3", 100),
            ("3.3.3.3", 100),
        ]

        stats = aggregate_by_ip(records)

        self.assertEqual(stats["1.1.1.1"]["requests"], 2)
        self.assertEqual(stats["1.1.1.1"]["bytes"], 300)
        self.assertEqual(stats["2.2.2.2"]["requests"], 1)
        self.assertEqual(stats["2.2.2.2"]["bytes"], 300)
        self.assertEqual(stats["3.3.3.3"]["requests"], 3)
        self.assertEqual(stats["3.3.3.3"]["bytes"], 300)

    def test_compute_report_sorting(self):
        stats = {
            "1.1.1.1": {"requests": 5, "bytes": 500},
            "2.2.2.2": {"requests": 10, "bytes": 1000},
        }

        report = compute_report(stats)

        self.assertEqual(report[0]["ip_address"], "2.2.2.2")
        self.assertEqual(report[1]["ip_address"], "1.1.1.1")


if __name__ == "__main__":
    unittest.main()
