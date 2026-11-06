"""Command-line entry point for the Air Quality advanced pipeline."""

import argparse
import json

from air_quality.workflows import AdvancedPipelineConfig, run_advanced


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Air Quality advanced pipeline")
    return parser.parse_args()


def main() -> None:
    parse_args()
    config = AdvancedPipelineConfig()
    metrics = run_advanced(config)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
