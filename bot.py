name: YT Shorts Bot

on:
  schedule:
    - cron: "*/5 * * * *"
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install requests
        run: pip install requests

      - name: Run bot
        run: python bot.py
        env:
          API_KEY: ${{ secrets.API_KEY }}
          WEBHOOK: ${{ secrets.WEBHOOK }}

      - name: Commit sent file
        run: |
          git config --local user.email "bot@github.com"
          git config --local user.name "GitHub Bot"
          git add sent_videos.txt
          git commit -m "update sent list" || echo "no changes"
          git push
