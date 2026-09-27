<div dir="rtl">

# ImageOptimizer — الدليل العربي

ImageOptimizer أداة سطر أوامر مكتوبة ببايثون لتحسين الصور محليًا، والتحويل بين JPEG وPNG وWebP، وتغيير الأبعاد، ومعالجة مجلدات كاملة من دون رفع الملفات إلى خدمة خارجية.

## التثبيت

</div>

~~~bash
git clone https://github.com/rad03i2/imageoptimizer.git
cd imageoptimizer
python -m venv .venv
python -m pip install -e .
~~~

<div dir="rtl">

يتطلب Python 3.10+ وPillow 10+.

## الوظائف الحالية

- تحسين JPEG وPNG وWebP.
- التحويل بين الصيغ الثلاث.
- تحديد أقصى عرض أو ارتفاع مع الحفاظ على نسبة الأبعاد.
- معالجة المجلدات والمجلدات الفرعية.
- تصحيح اتجاه EXIF قبل المعالجة.
- حماية ملفات الإخراج الموجودة إلا عند استخدام <code>--overwrite</code>.
- منع تعديل الصورة الأصلية في مكانها.
- حذف metadata افتراضيًا أو الاحتفاظ ببيانات EXIF/ICC المدعومة.
- تحويل الشفافية إلى خلفية محددة عند إنشاء JPEG.
- معاينة العمليات عبر <code>--dry-run</code>.
- إنشاء تقرير JSON.

## أمثلة

</div>

~~~bash
imageoptimizer photo.jpg -o optimized/photo.jpg --quality 82
imageoptimizer photo.png -o optimized/photo.webp --format webp --max-width 1600 --quality 80
imageoptimizer ./photos -o ./optimized --recursive --format webp --report report.json
imageoptimizer ./photos -o ./optimized --recursive --dry-run
~~~

<div dir="rtl">

## سلامة الملفات

يجب أن يختلف مسار الإخراج عن الصورة الأصلية. إذا كان ملف الإخراج موجودًا يتوقف البرنامج إلا عند استخدام <code>--overwrite</code>. تُكتب النتيجة أولًا إلى ملف مؤقت ثم تُنقل إلى الوجهة بعد نجاح الترميز.

## الخصوصية والبيانات الوصفية

تُحذف metadata افتراضيًا. خيار <code>--keep-metadata</code> يحاول الاحتفاظ ببيانات EXIF وICC المدعومة، وقد تتضمن البيانات الأصلية معلومات موقع أو جهاز حساسة.

## التقارير

يتضمن تقرير JSON مسارات المصدر والإخراج، الأحجام، الصيغ، الأبعاد النهائية، البايتات المحفوظة، نسبة التوفير المحسوبة، والإجماليات. لا توجد نسبة ضغط مضمونة.

## الاختبارات

</div>

~~~bash
python -m pip install -e ".[dev]"
ruff check src tests
pytest -q
~~~

<div dir="rtl">

يعمل CI على Ubuntu وWindows وmacOS مع Python 3.10 و3.12 و3.13.

## الحدود الحالية

لا ينفذ المشروع حاليًا تحسين GIF/WebP المتحرك، أو rasterization لـSVG، أو صيغ RAW، أو واجهة سطح مكتب أو خدمة ويب.

## المطور

**رضوان عبدالهادي** · **Radwan Abd alhady Ahmed** · [@rad03i2](https://github.com/rad03i2)

المشروع مرخص وفق MIT.

</div>
