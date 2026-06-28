from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from app.leadership.x5 import run_x5
payload = run_x5()
print(payload['summary'])
