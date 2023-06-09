#!/bin/bash
git fetch
git pull
start_time=$SECONDS
git add .
git commit -m "commit $(date)"
# git branch -M main
# git remote add origin git@github.com:garyfurash/2023-dezoomcamp.git
git push -u origin main
elapsed=$(( SECONDS - start_time ))
echo "Finish! $elapsed seconds to complete."