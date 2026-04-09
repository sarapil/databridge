# DataBridge — FAQ / الأسئلة الشائعة

## General / عام

**Q: What data sources does DataBridge support?**
A: CSV files, REST APIs, databases (MySQL/PostgreSQL), FTP, and SFTP. The connector framework is extensible for custom sources.

**س: ما مصادر البيانات التي يدعمها DataBridge؟**
ج: ملفات CSV، واجهات REST API، قواعد البيانات (MySQL/PostgreSQL)، FTP، و SFTP. إطار الموصلات قابل للتوسيع لمصادر مخصصة.

---

**Q: How does auto-mapping work?**
A: The MappingService compares source fields with target DocType fields using name similarity. It assigns a confidence score (0-100) and suggests the best matches.

**س: كيف يعمل التعيين التلقائي؟**
ج: تقارن خدمة التعيين حقول المصدر مع حقول DocType المستهدف باستخدام تشابه الأسماء، وتعيّن درجة ثقة (0-100) وتقترح أفضل التطابقات.

---

**Q: Can I schedule recurring imports?**
A: Yes. Use the Sync module to create sync profiles with cron-based schedules. The system handles conflict detection and resolution.

---

**Q: How are import errors handled?**
A: Each failed row is logged in DB Import Error with the row number, field, and error message. You can fix and re-import only the failed rows.

---

**Q: Does DataBridge support migration rollback?**
A: Yes. Migration Plans track each step, and the Migration Log allows you to identify what was imported for manual rollback.
