"""Per-harness coverage: every manifest's paths, entrypoints, and installer targets."""
import glob, json, os, subprocess, pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFESTS = sorted(glob.glob(os.path.join(ROOT, ".*-plugin", "plugin.json"))) + [
    os.path.join(ROOT, ".gemini", "extension.json"),
    os.path.join(ROOT, "gemini-extension.json"),
    os.path.join(ROOT, ".pi", "plugin.json"),
]

def test_every_harness_has_manifest():
    assert len(MANIFESTS) >= 15, f"expected >=15, found {len(MANIFESTS)}"

GEMINI = {os.path.join(ROOT, ".gemini", "extension.json"), os.path.join(ROOT, "gemini-extension.json")}

@pytest.mark.parametrize("manifest", MANIFESTS, ids=lambda p: os.path.relpath(p, ROOT))
def test_manifest_schema(manifest):
    data = json.load(open(manifest))
    if manifest in GEMINI:
        assert os.path.isfile(os.path.join(ROOT, data["contextFileName"])), manifest
    else:
        for key in ("skills", "agents", "commands"):
            assert os.path.isdir(os.path.join(ROOT, data[key])), f"{manifest}: {key} dir missing"
        assert os.path.isfile(os.path.join(ROOT, data["hooks"])), f"{manifest}: hooks file missing"
        assert os.path.isfile(os.path.join(ROOT, data["entrypoint"])), manifest

def test_manifest_versions_consistent():
    versions = {json.load(open(p))["version"] for p in MANIFESTS}
    assert len(versions) == 1, f"drift across manifests: {versions}"

HARNESS_TARGETS = ["claude", "opencode", "grok", "qwen", "factory", "custom-dest"]

@pytest.mark.parametrize("target", HARNESS_TARGETS)
def test_installer_dry_run_all_targets(target, tmp_path):
    src = os.path.join(ROOT, "scripts", "install.sh")
    env = dict(os.environ, HOME=str(tmp_path))
    argument = str(tmp_path / "custom-dest") if target == "custom-dest" else target
    r = subprocess.run(["bash", "-n", src], env=env, capture_output=True, text=True)
    assert r.returncode == 0
    r = subprocess.run(["bash", src, argument, "--dry-run"], env=env, capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0, r.stderr
    assert "dry-run" in r.stderr
    assert not (tmp_path / ".claude").exists()
    expected = {"claude": ".claude", "opencode": ".config/opencode", "grok": ".grok", "qwen": ".qwen", "factory": ".factory"}.get(target, "custom-dest")
    assert str(tmp_path / expected) in r.stderr

def test_marketplace_manifest_valid():
    data = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))
    assert data["plugins"], "marketplace lists no plugins"
    plugin = data["plugins"][0]
    assert os.path.isdir(os.path.join(ROOT, plugin["source"]))

def test_marketplace_version_matches_plugins():
    mp = json.load(open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")))["plugins"][0]["version"]
    pj = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))["version"]
    assert mp == pj
