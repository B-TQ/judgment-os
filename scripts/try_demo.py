"""Convenience launcher: offline only, no installs or credential reads."""
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys


def main():
    if sys.version_info < (3, 11):
        print("Python 3.11+ required / 需要 Python 3.11 或更新版本")
        return 1
    root = Path(__file__).resolve().parents[1]
    out = "runs/quickstart-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S-%f")
    print("Judgment OS / 离线体验：不安装软件，不读取密钥，不调用模型。", flush=True)
    commands = [("doctor",), ("demo", "--out", out),
                ("check", "--case", "Q01", "--answer", "examples/quickstart/correct.json")]
    for args in commands:
        result = subprocess.run([sys.executable, "-X", "utf8", "-B", str(root / "judgment.py"), *args], cwd=root)
        if result.returncode:
            return result.returncode
    print("Done / 完成。See / 查看: " + str(root / out / "START_HERE.md"))
    print("Authored software fixtures, not model-performance evidence / 人工软件示例，不是模型效果证据。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
