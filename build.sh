# build.sh
#!/usr/bin/env bash
pip install -r requirements.txt
python scripts/fetch_events_grist.py
hugo --minify --gc --buildFuture