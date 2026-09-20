# Security Policy / سياسة الأمان

ImageOptimizer is designed for local processing and makes no network requests. Treat image files as untrusted input and keep Pillow updated because image decoders process complex binary formats.

## Reporting a vulnerability

Please do not publish exploitable details in a public issue before a fix is available. Contact the maintainer through the GitHub profile/repository channels and include reproduction steps, affected versions, and impact. Do not include real private images or credentials in reports.

## Supported versions

The latest release/main branch receives security fixes.

## Privacy

Metadata is removed by default. `--keep-metadata` intentionally preserves supported metadata and may therefore retain location/device information present in a source image.

## العربية

المشروع مصمم لمعالجة الصور محليًا ولا يجري طلبات شبكية. تعامل مع الصور كمدخلات غير موثوقة وحافظ على تحديث Pillow. عند اكتشاف ثغرة، لا تنشر تفاصيل قابلة للاستغلال قبل توفر إصلاح؛ تواصل عبر قنوات المستودع/حساب GitHub مع خطوات إعادة المشكلة وتأثيرها، ومن دون إرفاق صور خاصة أو بيانات اعتماد حقيقية.

تُحذف البيانات الوصفية افتراضيًا. خيار `--keep-metadata` قد يحتفظ عمدًا بمعلومات حساسة موجودة أصلًا مثل بيانات الموقع أو الجهاز.
