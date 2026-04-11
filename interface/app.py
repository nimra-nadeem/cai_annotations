"""Simple Flask app for ruleset intent-preservation annotation."""
import json
import os
import time
from pathlib import Path
from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ANNOTATIONS_DIR = ROOT / "annotations"
ANNOTATIONS_DIR.mkdir(exist_ok=True)

DEFAULT_RULESET_DESCRIPTION = (
    "This is a model spec ruleset used for AI alignment, particularly for "
    "RLAIF, where judge models use the ruleset to identify problematic AI "
    "behavior. We are evaluating whether automatically revised versions of "
    "the ruleset preserve the intent of the original."
)

app = Flask(__name__)


def load_jsonl(path: Path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def discover_pairs():
    """Return list of pairs from `data/sets/<set_name>/`.

    Each set must contain:
      original_ruleset.jsonl
      revised_rulesets/*.jsonl
    """
    pairs = []
    sets_dir = DATA / "sets"
    for set_dir in sorted(sets_dir.iterdir()):
        if not set_dir.is_dir():
            continue
        orig_path = set_dir / "original_ruleset.jsonl"
        rev_dir = set_dir / "revised_rulesets"
        if not orig_path.exists() or not rev_dir.is_dir():
            continue
        orig_rules = load_jsonl(orig_path)
        description = (set_dir / "description.txt").read_text().strip()
        for rev_path in sorted(rev_dir.glob("*.jsonl")):
            pairs.append({
                "original_name": set_dir.name,
                "revised_name": rev_path.stem,
                "original_rules": orig_rules,
                "revised_rules": load_jsonl(rev_path),
                "description": description,
            })
    return pairs


PAIRS = discover_pairs()


@app.route("/")
def index():
    pair_keys = [
        {"original_name": p["original_name"], "revised_name": p["revised_name"]}
        for p in PAIRS
    ]
    return render_template(
        "index.html",
        description=DEFAULT_RULESET_DESCRIPTION,
        n_pairs=len(PAIRS),
        pair_keys=pair_keys,
    )


@app.route("/api/pair/<int:idx>")
def get_pair(idx):
    if idx < 0 or idx >= len(PAIRS):
        return jsonify({"error": "out of range"}), 404
    return jsonify({**PAIRS[idx], "index": idx, "total": len(PAIRS)})


@app.route("/api/annotate", methods=["POST"])
def annotate():
    payload = request.get_json()
    annotator = payload.get("annotator", "anonymous").strip() or "anonymous"
    safe = "".join(c for c in annotator if c.isalnum() or c in "-_")
    out = ANNOTATIONS_DIR / f"annotations_{safe}.jsonl"
    record = {
        "annotator": annotator,
        "original_name": payload["original_name"],
        "revised_name": payload["revised_name"],
        "score": payload["score"],  # -1, 0, or 1
        "label": payload["label"],  # "yes" / "unsure" / "no"
        "feedback": payload.get("feedback", ""),
        "timestamp": time.time(),
    }
    with open(out, "a") as f:
        f.write(json.dumps(record) + "\n")
    return jsonify({"ok": True, "saved_to": str(out.relative_to(ROOT))})


@app.route("/api/annotations/<annotator>")
def get_annotations(annotator):
    safe = "".join(c for c in annotator if c.isalnum() or c in "-_")
    path = ANNOTATIONS_DIR / f"annotations_{safe}.jsonl"
    if not path.exists():
        return jsonify({"annotations": {}})
    records = load_jsonl(path)
    latest = {}
    for r in records:
        key = f"{r['original_name']}:{r['revised_name']}"
        latest[key] = {
            "score": r["score"],
            "label": r["label"],
            "feedback": r.get("feedback", ""),
        }
    return jsonify({"annotations": latest})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
