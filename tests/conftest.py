import sys
from pathlib import Path


# add src dir so tests work
src = Path(__file__).parent.with_name('src')
assert src.is_dir(), src
if str(src) not in sys.path:
    sys.path.append(str(src))
