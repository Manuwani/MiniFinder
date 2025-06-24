# frontend/run_java.py
import subprocess
import os

def run_pattern_search(algorithm, text, pattern):
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
    input_data = f"{algorithm}\n{text}\n{pattern}"

    result = subprocess.run(
        ['java', '-cp', backend_dir, 'PatternMatcher'],
        input=input_data,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {"error": result.stderr.strip()}

    output = result.stdout.splitlines()
    parsed = {"positions": [], "matches": 0, "time_ms": 0}

    for line in output:
        if line.startswith("POSITIONS:"):
            raw = line.replace("POSITIONS:", "").replace(",", " ")
            parsed["positions"] = [int(x) for x in raw.split() if x.isdigit()]
        elif line.startswith("MATCHES:"):
            parsed["matches"] = int(line.replace("MATCHES:", "").strip())
        elif line.startswith("TIME_MS:"):
            parsed["time_ms"] = int(line.replace("TIME_MS:", "").strip())

    return parsed
