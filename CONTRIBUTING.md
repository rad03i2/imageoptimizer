# Contributing to ImageOptimizer

Keep changes focused, safe for user files, and tested when behavior changes.

## Setup

~~~bash
python -m pip install -e ".[dev]"
~~~

## Required checks

~~~bash
ruff check src tests
pytest -q
~~~

## Principles

- Preserve the no-in-place-write rule.
- Do not weaken existing-output protection without explicit design discussion.
- Add tests for discovery, conversion, resizing, metadata, reporting, or path changes.
- Do not introduce image uploads as an incidental dependency.
- Do not commit private images, credentials, generated collections, or incompatible third-party assets.
- Keep current capabilities separate from proposed features.
- Document user-visible CLI changes.

## العربية

يجب أن تبقى المساهمات آمنة على ملفات المستخدم، مع تشغيل Ruff والاختبارات وإضافة اختبارات لأي تغيير سلوكي. حافظ على منع الكتابة فوق الصورة الأصلية وحماية ملفات الإخراج، ولا تضف رفعًا شبكيًا للصور بصورة جانبية غير موثقة.

## Maintainer

**Radwan Abd alhady Ahmed** · **رضوان عبدالهادي** · [@rad03i2](https://github.com/rad03i2)
