#!/usr/bin/env python3
"""Generate Software Bill of Materials (SBOM) for Dealix.

Generates SBOM in CycloneDX JSON format for both Python and Node.js dependencies.
Output: docs/SBOM.json
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def get_python_packages() -> list[dict]:
    """Get Python packages from pip list."""
    try:
        result = subprocess.run(
            ["pip", "list", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        print("⚠️  Could not get Python packages", file=sys.stderr)
        return []

def get_npm_packages() -> list[dict]:
    """Get npm packages from package-lock.json."""
    packages = []
    lock_files = [
        Path("package-lock.json"),
        Path("frontend/package-lock.json"),
        Path("apps/web/package-lock.json"),
    ]

    for lock_file in lock_files:
        if not lock_file.exists():
            continue

        try:
            with lock_file.open() as f:
                data = json.load(f)
                if "packages" in data:
                    for pkg_name, pkg_data in data["packages"].items():
                        if pkg_name and pkg_data.get("version"):
                            packages.append({
                                "name": pkg_name,
                                "version": pkg_data["version"],
                                "type": "npm",
                            })
        except (json.JSONDecodeError, KeyError):
            continue

    return packages

def create_cyclonedx_sbom(python_pkgs: list[dict], npm_pkgs: list[dict]) -> dict:
    """Create CycloneDX format SBOM."""
    components = []

    for pkg in python_pkgs:
        components.append({
            "type": "library",
            "name": pkg["name"],
            "version": pkg["version"],
            "purl": f"pkg:pypi/{pkg['name']}@{pkg['version']}",
        })

    for pkg in npm_pkgs:
        components.append({
            "type": "library",
            "name": pkg["name"],
            "version": pkg["version"],
            "purl": f"pkg:npm/{pkg['name']}@{pkg['version']}",
        })

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "version": 1,
        "metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tools": [
                {
                    "vendor": "dealix",
                    "name": "sbom-generator",
                    "version": "1.0.0",
                }
            ],
            "component": {
                "type": "application",
                "name": "Dealix",
                "version": "1.0.0",
            },
        },
        "components": components,
    }

def main() -> int:
    """Generate and write SBOM."""
    print("📦 Generating Software Bill of Materials...")

    python_pkgs = get_python_packages()
    npm_pkgs = get_npm_packages()

    sbom = create_cyclonedx_sbom(python_pkgs, npm_pkgs)

    output_path = Path("docs/SBOM.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w") as f:
        json.dump(sbom, f, indent=2)

    print(f"✅ SBOM generated: {output_path}")
    print(f"   - Python packages: {len(python_pkgs)}")
    print(f"   - Node.js packages: {len(npm_pkgs)}")
    print(f"   - Total components: {len(sbom['components'])}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
