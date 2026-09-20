# ImageOptimizer

A local-first Python image optimization toolkit for shrinking images, converting formats, resizing assets, and processing entire folders without uploading files to a third-party service.

**Author:** Radwan Abdulhadi Ahmed · رضوان عبدالهادي أحمد · [@rad03i2](https://github.com/rad03i2)

## Why ImageOptimizer?

Websites, portfolios, documentation, and archives often contain images that are much larger than necessary. ImageOptimizer provides a reproducible command-line workflow for optimizing JPEG, PNG and WebP images while keeping originals untouched by default.

## Features

- Optimize JPEG, PNG and WebP files locally.
- Convert between JPEG, PNG and WebP.
- Resize by maximum width/height while preserving aspect ratio.
- Batch-process a directory, optionally recursively.
- Dry-run mode to preview every planned output.
- Safe output policy: existing files are not overwritten unless `--overwrite` is explicitly supplied.
- EXIF orientation correction before processing.
- Optional metadata preservation (`--keep-metadata`); metadata is stripped by default for smaller, more private outputs.
- JPEG transparency handling with a configurable background color.
- JSON processing report with input/output byte counts and savings.
- Deterministic exit codes and useful validation errors.

## Requirements

- Python 3.10+
- Pillow 10+

## Installation

```bash
git clone https://github.com/rad03i2/imageoptimizer.git
cd imageoptimizer
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -e .
```

For development and tests:

```bash
python -m pip install -e ".[dev]"
pytest
```

## Usage

Optimize one image:

```bash
imageoptimizer photo.jpg -o optimized/photo.jpg --quality 82
```

Convert and resize:

```bash
imageoptimizer photo.png -o optimized/photo.webp --format webp --max-width 1600 --max-height 1200 --quality 80
```

Batch process a folder:

```bash
imageoptimizer ./photos -o ./optimized --recursive --format webp --quality 80 --report report.json
```

Preview without writing anything:

```bash
imageoptimizer ./photos -o ./optimized --recursive --dry-run
```

Use `imageoptimizer --help` for all options.

## Safety & privacy

Processing happens locally. ImageOptimizer performs no network requests. Originals are never modified in place: the output path/directory must differ from the input. Existing outputs are protected unless `--overwrite` is given. Metadata is stripped by default; use `--keep-metadata` only when you intentionally want EXIF/ICC information retained.

## Project structure

```text
src/imageoptimizer/
  __init__.py      Package metadata
  core.py          Validation and image processing engine
  cli.py           Command-line interface
  report.py        Processing result/report models
tests/             Automated tests
.github/workflows/ CI test workflow
```

## Testing

```bash
pytest -q
```

CI runs the test suite on Linux, Windows and macOS for supported Python versions.

## Limitations

- Animated GIF/animated WebP optimization is intentionally not implemented; the tool focuses on still JPEG/PNG/WebP images.
- SVG and RAW camera formats are not rasterized.
- Compression savings depend on the source image and chosen format/quality.
- Metadata preservation is best-effort because not every metadata block is valid in every destination format.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security-sensitive reports should follow [SECURITY.md](SECURITY.md).

## License

MIT License. See [LICENSE](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)

---

# العربية

## ما هو ImageOptimizer؟

**ImageOptimizer** أداة بايثون محلية لتحسين الصور وتقليل أحجامها وتحويل صيغها وتغيير أبعادها ومعالجة مجلدات كاملة، من دون رفع الصور إلى أي خدمة خارجية.

## لماذا هذا المشروع؟

تحتوي المواقع ومعارض الأعمال والوثائق والأرشيفات غالبًا على صور أكبر من الحاجة. يوفر المشروع طريقة واضحة وقابلة للتكرار لتحسين صور JPEG وPNG وWebP مع إبقاء الملفات الأصلية دون تعديل افتراضيًا.

## المزايا

- تحسين JPEG وPNG وWebP محليًا.
- التحويل بين JPEG وPNG وWebP.
- تحديد أقصى عرض وارتفاع مع الحفاظ على نسبة الأبعاد.
- معالجة مجلد كامل مع خيار البحث داخل المجلدات الفرعية.
- وضع `--dry-run` لمعاينة العمليات قبل الكتابة.
- عدم استبدال ملف موجود إلا عند تمرير `--overwrite` صراحةً.
- تصحيح اتجاه الصورة اعتمادًا على EXIF قبل المعالجة.
- حذف البيانات الوصفية افتراضيًا للخصوصية وتقليل الحجم، مع خيار الاحتفاظ بها.
- معالجة الشفافية عند التحويل إلى JPEG بخلفية قابلة للتحديد.
- تقرير JSON يتضمن الحجم قبل وبعد ونسبة التوفير.
- أخطاء تحقق واضحة ورموز خروج مناسبة للسكربتات والأتمتة.

## التثبيت

```bash
git clone https://github.com/rad03i2/imageoptimizer.git
cd imageoptimizer
python -m venv .venv
python -m pip install -e .
```

للتطوير والاختبارات:

```bash
python -m pip install -e ".[dev]"
pytest
```

## أمثلة الاستخدام

تحسين صورة واحدة:

```bash
imageoptimizer photo.jpg -o optimized/photo.jpg --quality 82
```

تحويل الصورة إلى WebP مع تصغير الأبعاد:

```bash
imageoptimizer photo.png -o optimized/photo.webp --format webp --max-width 1600 --max-height 1200 --quality 80
```

معالجة مجلد كامل وإنتاج تقرير:

```bash
imageoptimizer ./photos -o ./optimized --recursive --format webp --quality 80 --report report.json
```

المعاينة من دون كتابة ملفات:

```bash
imageoptimizer ./photos -o ./optimized --recursive --dry-run
```

## الخصوصية والأمان

كل المعالجة محلية ولا ينفذ البرنامج طلبات شبكية. لا يعدل البرنامج الصور الأصلية في مكانها، ويحمي الملفات الموجودة من الاستبدال ما لم يطلب المستخدم ذلك صراحةً. تُحذف البيانات الوصفية افتراضيًا؛ استخدم `--keep-metadata` فقط عند الحاجة إليها.

## الاختبارات

```bash
pytest -q
```

يتضمن المستودع سير عمل CI لاختبار المشروع على Linux وWindows وmacOS.

## القيود

- لا يعالج الرسوم المتحركة في GIF/WebP؛ التركيز على الصور الثابتة.
- لا يحول SVG أو صيغ RAW الخاصة بالكاميرات.
- مقدار تقليل الحجم يعتمد على الصورة الأصلية والصيغة والجودة المختارة.
- الاحتفاظ بالبيانات الوصفية يعتمد على دعم صيغة الإخراج لها.

## المساهمة والترخيص

راجع [CONTRIBUTING.md](CONTRIBUTING.md) للمساهمة و[SECURITY.md](SECURITY.md) للإبلاغ الأمني. المشروع مرخص وفق MIT، والتفاصيل في [LICENSE](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)
