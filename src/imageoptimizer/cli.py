from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .core import ImageOptimizerError, Options, discover_images, optimize_image, output_path_for
from .report import write_report


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="imageoptimizer", description="Optimize, convert and resize images locally.")
    p.add_argument("input", type=Path, help="Image file or directory")
    p.add_argument("-o", "--output", required=True, type=Path, help="Output file or directory")
    p.add_argument("--format", choices=["jpeg", "png", "webp"], dest="output_format")
    p.add_argument("--quality", type=int, default=82, help="JPEG/WebP quality (1-100; default 82)")
    p.add_argument("--max-width", type=int)
    p.add_argument("--max-height", type=int)
    p.add_argument("--recursive", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--keep-metadata", action="store_true")
    p.add_argument("--background", default="#ffffff", help="Background used when flattening transparency to JPEG")
    p.add_argument("--dry-run", action="store_true", help="Show planned outputs without writing")
    p.add_argument("--report", type=Path, help="Write JSON report after successful processing")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    options = Options(
        quality=args.quality, output_format=args.output_format, max_width=args.max_width,
        max_height=args.max_height, overwrite=args.overwrite, keep_metadata=args.keep_metadata,
        background=args.background,
    )
    try:
        options.validate()
        files = discover_images(args.input, args.recursive)
        if not files:
            raise ImageOptimizerError("no supported images found")
        planned = [(f, output_path_for(f, args.input, args.output, args.output_format)) for f in files]
        for source, output in planned:
            if source.resolve() == output.resolve():
                raise ImageOptimizerError("output must differ from input; in-place writes are not allowed")
        if args.dry_run:
            for source, output in planned:
                print(f"DRY-RUN {source} -> {output}")
            return 0

        results = []
        for source, output in planned:
            result = optimize_image(source, output, options)
            results.append(result)
            print(f"OK {source} -> {output} ({result.savings_percent:+.2f}% saved)")
        if args.report:
            write_report(args.report, results)
            print(f"Report: {args.report}")
        total_in = sum(r.input_bytes for r in results)
        total_out = sum(r.output_bytes for r in results)
        print(f"Processed {len(results)} image(s): {total_in} -> {total_out} bytes")
        return 0
    except ImageOptimizerError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
