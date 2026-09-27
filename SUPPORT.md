# Support

## Before opening an issue

1. Confirm Python 3.10 or newer is installed.
2. Install development dependencies:
   ~~~bash
   python -m pip install -e ".[dev]"
   ~~~
3. Run:
   ~~~bash
   ruff check src tests
   pytest -q
   ~~~
4. Reproduce the problem with a small, non-sensitive image whenever possible.

## What to include in a bug report

Provide:

- operating system;
- Python version;
- ImageOptimizer command;
- source format;
- destination format;
- relevant options;
- expected behavior;
- actual behavior;
- traceback or stderr output if available.

Do not attach private photographs or images containing personal information merely to reproduce a bug. A generated test image is preferred.

## Common checks

### Output already exists

Existing files are protected by default. Use <code>--overwrite</code> only when replacement is intentional.

### Output equals input

In-place writes are deliberately rejected. Choose another file or output directory.

### Transparency changed when converting to JPEG

JPEG has no alpha channel. ImageOptimizer flattens transparent pixels onto the configured <code>--background</code> color.

### Metadata disappeared

Metadata is removed by default. Use <code>--keep-metadata</code> only when preserving supported EXIF/ICC data is intentional.

### Savings are small or negative

Compression results depend on the source image, destination format, image dimensions, and selected quality. Re-encoding an already optimized file can produce little benefit or even a larger output.

## Security

Do not publish exploitable decoder problems, credentials, or private images in a public issue. Follow [SECURITY.md](SECURITY.md).

## Feature requests

Explain the workflow problem first, then the proposed feature. Mention whether it introduces new formats, external services, metadata handling, or changes to write-safety behavior.
