from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_required_foundation_files_exist() -> None:
    required = [
        "README.md",
        "docker-compose.yml",
        "apps/web/src/app/page.tsx",
        "services/api/src/arasaac_platform/main.py",
        "services/mcp/src/safe_mcp/main.py",
        "openspec/changes/0001-project-foundation/spec.md",
    ]

    assert all((ROOT / path).is_file() for path in required)


def test_mcp_placeholder_has_no_registered_tools() -> None:
    source = (ROOT / "services/mcp/src/safe_mcp/main.py").read_text()

    assert "tools=[]" in source
    assert "subprocess" not in source
    assert "os.system" not in source
