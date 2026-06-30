from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from PIL import Image


LABEL_PATTERN = re.compile(r"\b([A-Z])\b", flags=re.IGNORECASE)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _resolve_path(path_value: str) -> Path:
    path = Path(path_value).expanduser()
    if path.is_absolute():
        return path
    return _repo_root() / path


def _iter_frame_paths(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        frames = value.get("frames")
        if isinstance(frames, list):
            for frame_path in frames:
                if isinstance(frame_path, str):
                    yield frame_path
        for child in value.values():
            yield from _iter_frame_paths(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_frame_paths(child)


def _json_from_response(response: str) -> dict[str, Any] | None:
    text = response.strip()
    if not text:
        return None

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        try:
            parsed = json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None

    return parsed if isinstance(parsed, dict) else None


def _choice_labels(doc: dict[str, Any]) -> list[str]:
    choices = doc.get("choices")
    if isinstance(choices, list) and choices:
        labels = [str(choice.get("label", "")).strip().upper() for choice in choices if isinstance(choice, dict)]
        return [label for label in labels if label]

    legal_clip_ids = doc.get("legal_clip_ids")
    if isinstance(legal_clip_ids, list) and legal_clip_ids:
        return [str(label).strip().upper() for label in legal_clip_ids if str(label).strip()]

    return ["A", "B", "C", "D"]


def _normalize_order(value: Any, legal_labels: list[str]) -> str | None:
    if isinstance(value, list):
        labels = [str(item).strip().upper() for item in value]
    else:
        labels = [match.upper() for match in LABEL_PATTERN.findall("" if value is None else str(value))]

    legal_set = set(legal_labels)
    labels = [label for label in labels if label in legal_set]
    if not labels:
        return None
    return ",".join(labels)


def _parse_label_response(response: str, legal_labels: list[str]) -> str | None:
    parsed = _json_from_response(response)
    if parsed:
        for key in ("answer_label", "answer"):
            candidate = parsed.get(key)
            if isinstance(candidate, str):
                label = candidate.strip().upper()
                if label in legal_labels:
                    return label

    labels = [match.upper() for match in LABEL_PATTERN.findall(response)]
    labels = [label for label in labels if label in set(legal_labels)]
    return labels[-1] if labels else None


def _parse_order_response(response: str, legal_labels: list[str]) -> str | None:
    parsed = _json_from_response(response)
    if parsed:
        for key in ("answer_sequence", "answer"):
            normalized = _normalize_order(parsed.get(key), legal_labels)
            if normalized:
                return normalized
    return _normalize_order(response, legal_labels)


def _target_for_doc(doc: dict[str, Any]) -> str:
    if doc.get("answer_format") == "clip_order":
        legal_labels = _choice_labels(doc)
        return _normalize_order(doc.get("answer_sequence", doc.get("answer")), legal_labels) or ""
    return str(doc.get("answer_label", doc.get("answer", ""))).strip().upper()


def cholec80_doc_to_visual(doc: dict[str, Any]) -> list[Image.Image]:
    visuals = []
    seen = set()
    for frame_path in _iter_frame_paths(doc):
        if frame_path in seen:
            continue
        seen.add(frame_path)
        resolved_path = _resolve_path(frame_path)
        with Image.open(resolved_path) as image:
            visuals.append(image.convert("RGB"))
    return visuals


def cholec80_doc_to_text(doc: dict[str, Any], lmms_eval_specific_kwargs: dict[str, Any] | None = None) -> str:
    kwargs = lmms_eval_specific_kwargs or {}
    pre_prompt = kwargs.get("pre_prompt", "")
    post_prompt = kwargs.get("post_prompt", "")

    prompt = str(doc.get("prompt") or doc.get("question") or "").replace("{images}", "").strip()
    return f"{pre_prompt}{prompt}{post_prompt}"


def cholec80_doc_to_target(doc: dict[str, Any]) -> str:
    return _target_for_doc(doc)


def cholec80_process_results(doc: dict[str, Any], results: list[Any]) -> dict[str, dict[str, Any]]:
    prediction = "" if not results or results[0] is None else str(results[0]).strip()
    legal_labels = _choice_labels(doc)
    target = _target_for_doc(doc)

    if doc.get("answer_format") == "clip_order":
        parsed_prediction = _parse_order_response(prediction, legal_labels)
    else:
        parsed_prediction = _parse_label_response(prediction, legal_labels)

    result = {
        "id": doc.get("id"),
        "task": doc.get("task"),
        "question_type": doc.get("question_type"),
        "answer_format": doc.get("answer_format", "answer_label"),
        "prediction": prediction,
        "parsed_prediction": parsed_prediction,
        "target": target,
        "is_correct": parsed_prediction == target,
        "is_answered": parsed_prediction is not None,
    }

    return {
        "cholec80_accuracy": result,
        "cholec80_answered_rate": result,
    }


def cholec80_aggregate_accuracy(results: list[dict[str, Any]]) -> float:
    if not results:
        return 0.0
    return sum(1.0 if result["is_correct"] else 0.0 for result in results) / len(results)


def cholec80_aggregate_answered_rate(results: list[dict[str, Any]]) -> float:
    if not results:
        return 0.0
    return sum(1.0 if result["is_answered"] else 0.0 for result in results) / len(results)
