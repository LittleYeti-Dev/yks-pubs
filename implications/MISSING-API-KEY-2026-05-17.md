# wp-implications-extract — SKIPPED (missing ANTHROPIC key)

**Reason:** neither `secrets.CLIVE_ANTHROP_KEY` nor `secrets.ANTHROPIC_API_KEY` is set in yks-pubs repo secrets.

To enable:
```bash
gh secret set CLIVE_ANTHROP_KEY -b'<api-key>' -R LittleYeti-Dev/yks-pubs
# OR
gh secret set ANTHROPIC_API_KEY -b'<api-key>' -R LittleYeti-Dev/yks-pubs
```

Once set, the next wp-level-up run will auto-fire this workflow and emit a real implications file.
