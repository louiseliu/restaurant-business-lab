"""Strip optional local-thread meta from an offline delivery copy; no runtime edits."""
import re,sys
from pathlib import Path
file=Path(sys.argv[1]);text=file.read_text();text,count=re.subn(r'<meta\b(?=[^>]*\bname\s*=\s*["\x27]data-app-local-thread["\x27])[^>]*>\n?','',text,flags=re.I)
file.write_text(text);print('Local metadata tags removed:',count)
