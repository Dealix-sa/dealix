"""
Hermes Trust module — AI Risk Controls library (Section 55).

كل control عبارة عن دالة فحص deterministic مرتبطة بـ control_id موحّد. هذا
يخلي الـ Trust Workspace قادر يعرض "أي control انتُهك آخر 24 ساعة" بدون
أن يفحص الكود الحي.
"""

from .controls import (
    Control,
    ControlLibrary,
    ControlSeverity,
    ControlVerdict,
    default_library,
)

__all__ = [
    "Control",
    "ControlLibrary",
    "ControlSeverity",
    "ControlVerdict",
    "default_library",
]
