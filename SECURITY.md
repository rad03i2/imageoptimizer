# Security Policy

ImageOptimizer is designed for local processing; the application code makes no network requests.

## Reporting

Use GitHub private security reporting when available. Do not publish exploitable details, private images, credentials, real EXIF location samples, or other sensitive material in public issues.

## Untrusted image input

Image decoders handle complex binary formats. Treat unknown images as untrusted and keep Pillow and Python security updates current.

## Privacy

Metadata is stripped by default. `--keep-metadata` intentionally attempts to retain supported EXIF/ICC data, which may contain location, time, or device information already present in the source.

## File safety

The implementation rejects in-place writes, protects existing outputs unless `--overwrite` is explicit, writes through a temporary output, removes that temporary file on encoding failure, and verifies final output dimensions.

These controls do not replace filesystem permissions, backups, sandboxing, or malware scanning.

## Scope

ImageOptimizer does not provide authentication, remote storage, or a web upload service. An embedding service must define its own upload limits, access controls, isolation, and content-security policy.
