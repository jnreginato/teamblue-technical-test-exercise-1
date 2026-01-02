import csv
import json
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


def compute_report(stats: Dict[str, Dict[str, int]]) -> List[Dict[str, float]]:
    """
    Computes percentages and returns a sorted report structure.
    """
    total_requests = sum(item["requests"] for item in stats.values())
    total_bytes = sum(item["bytes"] for item in stats.values())

    report = []

    for ip, data in stats.items():
        report.append({
            "ip_address": ip,
            "requests": data["requests"],
            "requests_pct": (data["requests"] / total_requests) * 100 if total_requests else 0,
            "bytes": data["bytes"],
            "bytes_pct": (data["bytes"] / total_bytes) * 100 if total_bytes else 0,
        })

    # Sort by requests DESC, then bytes DESC
    report.sort(
        key=lambda x: (x["requests"], x["bytes"]),
        reverse=True
    )

    return report


def write_csv(report: List[Dict[str, float]], output_path: str) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "IP Address",
            "Number of Requests",
            "Percentage of Total Requests",
            "Total Bytes Sent",
            "Percentage of Total Bytes",
        ])

        for row in report:
            writer.writerow([
                row["ip_address"],
                row["requests"],
                f"{row['requests_pct']:.2f}",
                row["bytes"],
                f"{row['bytes_pct']:.2f}",
            ])


def write_json(report: List[Dict[str, float]], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(report, jsonfile, indent=2)


def generate_report(
        input_log: str,
        output_file: str,
        output_format: str = "csv",
) -> None:
    records = parse_log_file(input_log)
    stats = aggregate_by_ip(records)
    report = compute_report(stats)

    if output_format == "json":
        write_json(report, output_file)
    else:
        write_csv(report, output_file)


if __name__ == "__main__":
    generate_report(
        input_log="logfiles/requests.log",
        output_file="reports/ipaddr.csv",
        output_format="csv",  # or "json"
    )
