import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    package = ROOT / "ultimate_loot_mod"
    archive = ROOT / "out" / "ultimate_loot_mod.sdkmod"
    archive.parent.mkdir(exist_ok=True)

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(package.rglob("*")):
            parts = path.relative_to(package).parts
            if path.is_file() and not any(p.startswith((".", "__pycache__")) for p in parts):
                zf.write(path, path.relative_to(ROOT).as_posix())

    print(f"Wrote {archive}")


if __name__ == "__main__":
    main()
