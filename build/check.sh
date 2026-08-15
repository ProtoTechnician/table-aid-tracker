#!/bin/bash
# extract the single <script> body from an html file and syntax-check it
f="${1:-/home/claude/abyss_tracker.html}"
python3 - "$f" <<'EOF'
import sys,io,re
p=sys.argv[1]
s=io.open(p,encoding='utf-8').read()
blocks=re.findall(r'<script>(.*?)</script>',s,re.S)
print("script blocks:",len(blocks))
io.open('/tmp/chk.js','w',encoding='utf-8').write('\n'.join(blocks))
EOF
node --check /tmp/chk.js && echo "SYNTAX OK"
