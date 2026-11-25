"""CLI for Semantic Chunk Boundary Aligner."""
import argparse
import json
from .core import SemanticChunkAligner


def main():
    parser = argparse.ArgumentParser(description="Semantic Chunk Boundary Aligner CLI")
    parser.add_argument("--max-chars", type=int, default=300, help="Target max chars per chunk")
    args = parser.parse_args()

    aligner = SemanticChunkAligner(max_chars=args.max_chars)
    sample = "# Guide\n## Setup\nRun pip install.\n```bash\npip install demo\n```\n## Usage\nCall run()."
    print(json.dumps(aligner.chunk(sample), indent=2))


if __name__ == "__main__":
    main()
