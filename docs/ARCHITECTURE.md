# ImageOptimizer Architecture

ImageOptimizer uses a direct local pipeline: discover files, validate intent, decode and normalize an image, transform it, encode through a temporary file, verify output, and return structured processing data.

## Components

### CLI — `src/imageoptimizer/cli.py`

Parses arguments, builds processing options, discovers files, plans output paths, supports dry-run, executes processing, optionally writes a JSON report, and maps expected errors to exit code 2.

### Core — `src/imageoptimizer/core.py`

Owns option validation, supported formats, file discovery, output path construction, JPEG transparency flattening, resizing, format-specific encoder settings, temporary output handling, and final dimension verification.

### Reports — `src/imageoptimizer/report.py`

`ProcessResult` stores paths, formats, byte sizes, and dimensions, and calculates saved bytes and savings percentage. `write_report` serializes per-file and aggregate totals to JSON.

## Pipeline

~~~text
source path
    │
    ▼
discover + validate
    │
    ▼
Pillow decode
    │
    ▼
EXIF orientation correction
    │
    ├── optional resize
    ├── optional conversion
    └── metadata policy
    │
    ▼
format-specific encode
    │
    ▼
temporary output
    │
    ▼
destination replace
    │
    ▼
dimension verification
    │
    ▼
ProcessResult
~~~

## Format behavior

- JPEG: configurable quality, optimized progressive output, transparency flattening when needed.
- PNG: optimization enabled, compression level 9.
- WebP: configurable quality, method 6.

## Safety model

In-place writes are rejected. Existing outputs require explicit overwrite permission. On an encoding error, the temporary file is removed. Successful outputs are reopened to verify dimensions.

## Tests

Current tests cover conversion/resize, transparent PNG to JPEG, overwrite protection, in-place rejection, quality validation, recursive discovery, relative output-tree planning, and report totals/savings.

## Network boundary

The running application code contains no upload client or remote-processing path. Image handling is local.
