from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageColor, ImageOps, UnidentifiedImageError

from .report import ProcessResult

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
FORMAT_EXTENSIONS = {"jpeg": ".jpg", "png": ".png", "webp": ".webp"}


class ImageOptimizerError(ValueError):
    """Raised for expected user-facing validation/processing errors."""


@dataclass(frozen=True)
class Options:
    quality: int = 82
    output_format: str | None = None
    max_width: int | None = None
    max_height: int | None = None
    overwrite: bool = False
    keep_metadata: bool = False
    background: str = "#ffffff"

    def validate(self) -> None:
        if not 1 <= self.quality <= 100:
            raise ImageOptimizerError("quality must be between 1 and 100")
        if self.output_format and self.output_format.lower() not in FORMAT_EXTENSIONS:
            raise ImageOptimizerError("format must be jpeg, png, or webp")
        if self.max_width is not None and self.max_width < 1:
            raise ImageOptimizerError("max-width must be positive")
        if self.max_height is not None and self.max_height < 1:
            raise ImageOptimizerError("max-height must be positive")
        try:
            ImageColor.getrgb(self.background)
        except ValueError as exc:
            raise ImageOptimizerError(f"invalid background color: {self.background}") from exc


def discover_images(source: Path, recursive: bool = False) -> list[Path]:
    if source.is_file():
        if source.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ImageOptimizerError(f"unsupported image extension: {source.suffix or '(none)'}")
        return [source]
    if not source.is_dir():
        raise ImageOptimizerError(f"input does not exist: {source}")
    iterator = source.rglob("*") if recursive else source.glob("*")
    return sorted(p for p in iterator if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)


def output_path_for(source_file: Path, source_root: Path, output_root: Path, fmt: str | None) -> Path:
    if source_root.is_file():
        if output_root.exists() and output_root.is_dir():
            base = output_root / source_file.name
        elif output_root.suffix:
            base = output_root
        else:
            base = output_root / source_file.name
    else:
        base = output_root / source_file.relative_to(source_root)
    if fmt:
        base = base.with_suffix(FORMAT_EXTENSIONS[fmt.lower()])
    return base


def _flatten_for_jpeg(image: Image.Image, background: str) -> Image.Image:
    if image.mode in {"RGBA", "LA"} or (image.mode == "P" and "transparency" in image.info):
        rgba = image.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, ImageColor.getrgb(background) + (255,))
        bg.alpha_composite(rgba)
        return bg.convert("RGB")
    return image.convert("RGB") if image.mode not in {"RGB", "L"} else image


def optimize_image(source: Path, output: Path, options: Options) -> ProcessResult:
    options.validate()
    source = source.resolve()
    output = output.resolve()
    if source == output:
        raise ImageOptimizerError("output must differ from input; in-place writes are not allowed")
    if output.exists() and not options.overwrite:
        raise ImageOptimizerError(f"output already exists: {output}")

    try:
        with Image.open(source) as opened:
            input_format = (opened.format or "unknown").upper()
            exif = opened.info.get("exif") if options.keep_metadata else None
            icc = opened.info.get("icc_profile") if options.keep_metadata else None
            image = ImageOps.exif_transpose(opened)
            image.load()
            image = image.copy()
    except (OSError, UnidentifiedImageError) as exc:
        raise ImageOptimizerError(f"cannot decode image: {source}") from exc

    if options.max_width or options.max_height:
        width_limit = options.max_width or image.width
        height_limit = options.max_height or image.height
        image.thumbnail((width_limit, height_limit), Image.Resampling.LANCZOS)

    fmt = (options.output_format or input_format).lower()
    if fmt == "jpg":
        fmt = "jpeg"
    if fmt not in FORMAT_EXTENSIONS:
        raise ImageOptimizerError(f"unsupported output format: {fmt}")
    if fmt == "jpeg":
        image = _flatten_for_jpeg(image, options.background)

    save_kwargs: dict = {}
    if fmt in {"jpeg", "webp"}:
        save_kwargs["quality"] = options.quality
    if fmt == "jpeg":
        save_kwargs.update(optimize=True, progressive=True)
    elif fmt == "png":
        save_kwargs.update(optimize=True, compress_level=9)
    elif fmt == "webp":
        save_kwargs["method"] = 6
    if exif:
        save_kwargs["exif"] = exif
    if icc:
        save_kwargs["icc_profile"] = icc

    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_name(f".{output.name}.tmp{FORMAT_EXTENSIONS[fmt]}")
    try:
        image.save(temp, format=fmt.upper(), **save_kwargs)
        temp.replace(output)
    except OSError as exc:
        temp.unlink(missing_ok=True)
        raise ImageOptimizerError(f"failed to write output: {output}") from exc
    finally:
        image.close()

    return ProcessResult(
        source=str(source), output=str(output), input_bytes=source.stat().st_size,
        output_bytes=output.stat().st_size, input_format=input_format,
        output_format=fmt.upper(), width=Image.open(output).width, height=Image.open(output).height,
    )
