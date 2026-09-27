# ImageOptimizer — English Guide

ImageOptimizer is a local-first Python CLI for optimizing still images, converting JPEG/PNG/WebP, resizing assets, and processing folders without uploading files to a third-party service.

## Install

~~~bash
git clone https://github.com/rad03i2/imageoptimizer.git
cd imageoptimizer
python -m venv .venv
python -m pip install -e .
~~~

Requirements: Python 3.10+ and Pillow 10+.

## Current capabilities

- Optimize JPEG, PNG, and WebP.
- Convert between those formats.
- Resize to maximum width/height while preserving aspect ratio.
- Process folders recursively.
- Correct EXIF orientation before processing.
- Protect existing outputs unless overwrite is explicit.
- Reject in-place writes.
- Strip metadata by default or preserve supported EXIF/ICC data.
- Flatten transparency to a configurable background when creating JPEG.
- Preview work with dry-run mode.
- Write JSON processing reports.

## Examples

~~~bash
imageoptimizer photo.jpg -o optimized/photo.jpg --quality 82
imageoptimizer photo.png -o optimized/photo.webp --format webp --max-width 1600 --quality 80
imageoptimizer ./photos -o ./optimized --recursive --format webp --report report.json
imageoptimizer ./photos -o ./optimized --recursive --dry-run
~~~

## File safety

The output must differ from the source. Existing output causes an error unless `--overwrite` is supplied. Encoding is written to a temporary sibling file before replacement of the destination.

## Metadata

Metadata is stripped by default. `--keep-metadata` attempts to retain supported EXIF and ICC blocks. Preserved metadata may include sensitive location/device information already present in the source.

## Reports

JSON reports contain source/output paths, byte counts, formats, dimensions, saved bytes, calculated savings percentage, and aggregate totals. Compression results vary by image and settings.

## Verification

~~~bash
python -m pip install -e ".[dev]"
ruff check src tests
pytest -q
~~~

CI covers Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

## Current limitations

Animated GIF/animated WebP optimization, SVG rasterization, RAW formats, a desktop GUI, and online processing are outside the current implementation.

## Docs

[Architecture](docs/ARCHITECTURE.md) · [Brand](docs/BRAND.md) · [Security](SECURITY.md) · [Contributing](CONTRIBUTING.md) · [Changelog](CHANGELOG.md)

## Author

**Radwan Abd alhady Ahmed** · **رضوان عبدالهادي** · [@rad03i2](https://github.com/rad03i2)

MIT licensed.
