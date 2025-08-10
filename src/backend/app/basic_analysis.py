from typing import Any, Dict, List


def basic_analyze_code_features(code: str) -> Dict[str, Any]:
    lines: List[str] = code.splitlines()

    comment_lines = [l for l in lines if l.strip().startswith("//")]
    blank_lines = [l for l in lines if not l.strip()]

    return {
        "loc": len(lines),
        "token_count": None,
        "cyclomatic_complexity": None,
        "functions": None,
        "comment_ratio": (len(comment_lines) / len(lines)) if lines else 0.0,
        "blank_ratio": (len(blank_lines) / len(lines)) if lines else 0.0,
    }


def basic_detect_ai_code(code: str, features: Dict[str, Any]) -> Dict[str, Any]:
    score = 0.0
    reasons: List[str] = []

    if float(features.get("comment_ratio", 0.0) or 0.0) > 0.15:
        score += 0.3
        reasons.append("Code được comment nhiều (Khả năng là AI-generated)")

    import re
    descriptive_names = len(re.findall(r"\b[a-zA-Z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\b", code))
    if descriptive_names > 3:
        score += 0.2
        reasons.append("Tên biến có ý nghĩa (Khả năng là AI-generated)")

    if "#include" in code and "int main()" in code and "return 0" in code:
        score += 0.2
        reasons.append("Có mẫu chuẩn (Khả năng là AI-generated)")

    if int(features.get("loc", 0) or 0) < 20:
        score -= 0.2
        reasons.append("Code ngắn (Khả năng là Human-written)")

    if score > 0.5:
        prediction = "AI-generated"
        confidence = min(0.95, score)
    elif score < 0.3:
        prediction = "Human-written"
        confidence = min(0.95, 1.0 - score)
    else:
        prediction = "Uncertain"
        confidence = 0.5

    return {
        "prediction": prediction,
        "confidence": round(confidence, 3),
        "reasoning": reasons[:3],
        "method_used": "heuristic-static",
    }


