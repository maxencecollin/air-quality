"""Command-line entry point for the Air Quality baseline pipeline."""

import argparse
import json

from air_quality.workflows import PipelineConfig, run_baseline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Air Quality baseline pipeline")
    parser.add_argument("--train-city", default="Kampala")
    parser.add_argument("--test-city", default="Nairobi")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = PipelineConfig(train_city=args.train_city, test_city=args.test_city)
    metrics = run_baseline(config)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
