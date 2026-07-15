"""
Relation extraction — lightweight subject-predicate-object triple extractor.
استخراج العلاقات بصيغة (موضوع، علاقة، مفعول).

Combines NER + verb-cue patterns. Bilingual. Designed for Dealix sales /
customer brain knowledge-graph ingestion (no LLM call needed for first
pass).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from dealix.intelligence.layers.ner import Entity, NERTagger


@dataclass(frozen=True)
class RelationTriple:
    subject: str
    predicate: str
    object: str
    confidence: float
    sentence: str
    subject_label: str = ""
    object_label: str = ""


# Verb cues that signal a relation type. Order matters — first match wins.
_PREDICATE_CUES: list[tuple[str, list[str]]] = [
    ("located_in", ["located in", "based in", "headquartered in", "في", "بـ", "مقرها"]),
    ("works_for", ["works for", "employed by", "يعمل لدى", "موظف في", "يعمل في"]),
    ("founded", ["founded", "launched", "established", "أسس", "أنشأ", "أسست"]),
    ("acquired", ["acquired", "bought", "purchased", "استحوذت على", "اشترى"]),
    ("partnered_with", ["partnered with", "partnership with", "شراكة مع", "تعاون مع"]),
    ("invested_in", ["invested in", "funded", "استثمر في", "موّل"]),
    ("priced_at", ["priced at", "costs", "for sale at", "بسعر", "بـ", "ثمنه"]),
    ("uses", ["uses", "powered by", "running on", "يستخدم", "تستعمل"]),
    ("ceo_of", ["ceo of", "chief executive of", "رئيس تنفيذي", "المدير التنفيذي"]),
    ("offers", ["offers", "provides", "sells", "يقدم", "تقدم", "تبيع"]),
    ("targets", ["targets", "serves", "يستهدف", "تستهدف"]),
    ("competes_with", ["competes with", "vs", "ينافس", "منافس"]),
    ("operates_in", ["operates in", "active in", "تعمل في", "ناشطة في"]),
]

_SENT_SPLIT = re.compile(r"(?<=[\.\?!؟])\s+|\n+")


class RelationExtractor:
    def __init__(self, ner: NERTagger | None = None) -> None:
        self._ner = ner or NERTagger()

    def extract(self, text: str) -> list[RelationTriple]:
        if not text:
            return []
        results: list[RelationTriple] = []
        for sent in _SENT_SPLIT.split(text):
            sent = sent.strip()
            if len(sent) < 8:
                continue
            entities = self._ner.tag(sent)
            sentence_low = sent.lower()
            for predicate, cues in _PREDICATE_CUES:
                cue_idx = -1
                cue_used = ""
                for cue in cues:
                    idx = sentence_low.find(cue)
                    if idx >= 0:
                        cue_idx = idx
                        cue_used = cue
                        break
                if cue_idx < 0:
                    continue
                # subject = entity just before cue; object = entity just after
                subj = self._nearest_entity_before(entities, cue_idx)
                obj = self._nearest_entity_after(entities, cue_idx + len(cue_used))
                if not subj:
                    subj = self._fallback_noun_before(sent, cue_idx)
                if not obj:
                    obj = self._fallback_noun_after(sent, cue_idx + len(cue_used))
                if not subj or not obj:
                    continue
                if subj.text == obj.text:
                    continue
                conf = 0.5 + 0.25 * min(subj.score, obj.score)
                results.append(
                    RelationTriple(
                        subject=subj.text,
                        predicate=predicate,
                        object=obj.text,
                        confidence=round(conf, 3),
                        sentence=sent,
                        subject_label=subj.label,
                        object_label=obj.label,
                    )
                )
        return self._dedupe(results)

    @staticmethod
    def _fallback_noun_before(sent: str, cue_idx: int) -> Entity | None:
        """Capitalized / non-stopword token chunk immediately before the cue."""
        head = sent[:cue_idx].rstrip()
        if not head:
            return None
        words = head.split()
        if not words:
            return None
        # Walk back collecting capitalized / Arabic tokens.
        chunk: list[str] = []
        for w in reversed(words):
            clean = w.strip(",.;:()[]")
            if not clean:
                continue
            first = clean[0]
            if first.isupper() or "؀" <= first <= "ۿ":
                chunk.insert(0, clean)
                continue
            break
        if not chunk:
            # fall back to the last word
            last = words[-1].strip(",.;:()[]")
            if last and len(last) > 1:
                chunk = [last]
        if not chunk:
            return None
        phrase = " ".join(chunk)
        start = head.rfind(phrase)
        if start < 0:
            start = max(0, cue_idx - len(phrase))
        return Entity(phrase, "NOUN", start, start + len(phrase), 0.4)

    @staticmethod
    def _fallback_noun_after(sent: str, idx: int) -> Entity | None:
        tail = sent[idx:].lstrip()
        if not tail:
            return None
        offset = sent.find(tail, idx)
        if offset < 0:
            offset = idx
        words = tail.split()
        if not words:
            return None
        chunk: list[str] = []
        for w in words:
            clean = w.strip(",.;:()[]?!")
            if not clean:
                continue
            first = clean[0]
            if first.isupper() or "؀" <= first <= "ۿ":
                chunk.append(clean)
                continue
            if chunk:
                break
        if not chunk:
            last = words[0].strip(",.;:()[]?!")
            if last:
                chunk = [last]
        if not chunk:
            return None
        phrase = " ".join(chunk)
        start = sent.find(phrase, offset)
        if start < 0:
            start = offset
        return Entity(phrase, "NOUN", start, start + len(phrase), 0.4)

    @staticmethod
    def _nearest_entity_before(entities: list[Entity], idx: int) -> Entity | None:
        candidates = [e for e in entities if e.end <= idx]
        return max(candidates, key=lambda e: e.end) if candidates else None

    @staticmethod
    def _nearest_entity_after(entities: list[Entity], idx: int) -> Entity | None:
        candidates = [e for e in entities if e.start >= idx]
        return min(candidates, key=lambda e: e.start) if candidates else None

    @staticmethod
    def _dedupe(triples: list[RelationTriple]) -> list[RelationTriple]:
        seen: set[tuple[str, str, str]] = set()
        out: list[RelationTriple] = []
        for t in triples:
            key = (t.subject, t.predicate, t.object)
            if key in seen:
                continue
            seen.add(key)
            out.append(t)
        return out
