"""Every plugin manifest is valid JSON with the required fields."""
import glob, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTS = sorted(glob.glob(os.path.join(ROOT, ".*-plugin", "*.json"))) + [
    os.path.join(ROOT, ".gemini", "extension.json"),
    os.path.join(ROOT, ".pi", "plugin.json"),
    os.path.join(ROOT, "gemini-extension.json"),
]
REQUIRED = {"name", "version", "description"}

def test_manifests_exist():
    assert len(MANIFESTS) >= 12, f"only {len(MANIFESTS)} manifests found"

def test_valid_json():
    for p in MANIFESTS:
        with open(p) as f:
            json.load(f)

def test_required_fields():
    for p in MANIFESTS:
        with open(p) as f:
            data = json.load(f)
        missing = REQUIRED - set(data)
        assert not missing, f"{os.path.basename(os.path.dirname(p))}: missing {missing}"

def test_entrypoint_exists():
    p = os.path.join(ROOT, ".claude-plugin", "plugin.json")
    entry = json.load(open(p))["entrypoint"]
    assert os.path.isfile(os.path.join(ROOT, entry)), f"entrypoint missing: {entry}"
