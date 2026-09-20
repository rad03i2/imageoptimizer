from pathlib import Path

import pytest
from PIL import Image

from imageoptimizer.core import (
    ImageOptimizerError, Options, discover_images, optimize_image, output_path_for,
)


def make_image(path: Path, mode="RGB", size=(120, 80)) -> None:
    image = Image.new(mode, size, (120, 40, 200, 128) if mode == "RGBA" else (120, 40, 200))
    image.save(path)
    image.close()


def test_resize_and_convert_to_webp(tmp_path):
    source = tmp_path / "source.png"
    output = tmp_path / "out.webp"
    make_image(source, size=(400, 200))
    result = optimize_image(source, output, Options(output_format="webp", max_width=100))
    assert output.exists()
    assert result.output_format == "WEBP"
    assert (result.width, result.height) == (100, 50)


def test_transparent_png_to_jpeg(tmp_path):
    source = tmp_path / "transparent.png"
    output = tmp_path / "flat.jpg"
    make_image(source, mode="RGBA")
    optimize_image(source, output, Options(output_format="jpeg"))
    with Image.open(output) as image:
        assert image.mode == "RGB"
        assert image.format == "JPEG"


def test_existing_output_is_protected(tmp_path):
    source = tmp_path / "source.png"
    output = tmp_path / "out.png"
    make_image(source)
    make_image(output)
    with pytest.raises(ImageOptimizerError, match="already exists"):
        optimize_image(source, output, Options())


def test_in_place_write_is_rejected(tmp_path):
    source = tmp_path / "source.png"
    make_image(source)
    with pytest.raises(ImageOptimizerError, match="in-place"):
        optimize_image(source, source, Options())


def test_quality_validation():
    with pytest.raises(ImageOptimizerError):
        Options(quality=0).validate()
    with pytest.raises(ImageOptimizerError):
        Options(quality=101).validate()


def test_discovery_respects_recursive_flag(tmp_path):
    make_image(tmp_path / "one.png")
    nested = tmp_path / "nested"
    nested.mkdir()
    make_image(nested / "two.jpg")
    assert [p.name for p in discover_images(tmp_path, False)] == ["one.png"]
    assert {p.name for p in discover_images(tmp_path, True)} == {"one.png", "two.jpg"}


def test_output_path_preserves_relative_tree(tmp_path):
    root = tmp_path / "input"
    source = root / "nested" / "a.png"
    output = tmp_path / "out"
    assert output_path_for(source, root, output, "webp") == output / "nested" / "a.webp"
