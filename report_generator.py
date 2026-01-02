from collections import defaultdict
from typing import Dict, List, Tuple


def parse_log_file(filepath: str) -> List[Tuple[str, int]]:
    """
    Reads the log file and returns a list of (ip, bytes) tuples
    considering only lines with STATUS == 'OK'.
    """
    records = []

    with open(filepath, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                timestamp, bytes_sent, status, ip = line.split(";")
                if status != "OK":
                    continue

                bytes_value = int(bytes_sent)
                if bytes_value < 0:
                    continue

                if not ip.strip():
                    continue

                records.append((ip, bytes_value))

            except ValueError:
                # Skip malformed lines safely
                continue

    return records


def aggregate_by_ip(records: List[Tuple[str, int]]) -> Dict[str, Dict[str, int]]:
    """
    Aggregates request count and total bytes per IP.
    """
    stats = defaultdict(lambda: {"requests": 0, "bytes": 0})

    for ip, bytes_sent in records:
        stats[ip]["requests"] += 1
        stats[ip]["bytes"] += bytes_sent

    return stats


def generate_report(
        input_log: str,
        output_file: str,
        output_format: str = "csv",
) -> None:
    records = parse_log_file(input_log)
    stats = aggregate_by_ip(records)
    print(stats)

    # compute_report
    # write_report(output_file, output_format)


if __name__ == "__main__":
    generate_report(
        input_log="logfiles/requests.log",
        output_file="reports/ipaddr.csv",
        output_format="csv",  # or "json"
    )
