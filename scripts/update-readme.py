import re
import subprocess

from pathlib import Path

ROOT = Path(__file__).parent.parent

readme = ROOT.joinpath("README.md").resolve(strict=True)

buffer = readme.read_text()

output = subprocess.check_output("python -mpydev --help", shell=True, encoding="utf-8")

pattern = """```console\nUsage:(.*?)```"""
replace = f"```console\n{output}```"

buffer, count = re.subn(pattern, replace, buffer, flags=re.DOTALL)

if count:
    print("Updating REAMDE.md ...")
    readme.write_text(buffer)

