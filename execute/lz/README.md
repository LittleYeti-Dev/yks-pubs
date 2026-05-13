# execute/lz/ — Landing Zone

**Purpose:** Cross-persona credential + artifact landing zone via this repo as transit hub. Universal pattern — every yks-* repo carries an `execute/lz/` to support cross-bench drops.

**Pattern:** TM (or any persona with rw on this repo) drops a file here via Contents API. Any persona that pulls this repo gets the file automatically. Receiving persona reads, moves to its bench (`.secrets/`, `.sandbox-creds/`, or wherever), and ideally deletes from the LZ in a follow-up commit once consumed.

**Lifecycle expectations:**
- Drops are point-in-time. Rotate when needed.
- Receiving persona should consume + remove (in a follow-up commit) once the artifact lands in the bench. Stale credentials in commit history are a known tradeoff of this pattern — acceptable per Yeti 2026-05-13 ("the mirror project we are building").
- DO NOT push to public forks. Visibility on each yks-* repo is the only safety boundary on this pattern (most yks-* repos are private; yks-pubs is the public PDF mirror — never drop credentials there).

**Consume protocol example (PAT drop into Clive's bench):**

```bash
cp execute/lz/github-pat-clive.txt ~/.secrets/github-pat-clive.txt
chmod 600 ~/.secrets/github-pat-clive.txt
# Follow-up commit to remove from LZ
git rm execute/lz/github-pat-clive.txt
git commit -m "execute/lz: consume + remove github-pat-clive.txt — landed in bench"
git push origin main
```

**Future automation:** The mirror-automation spec (yks-build #197 staging) will handle the drop → consume → remove cycle as a workflow_dispatch loop. This LZ is the manual precursor.

**Adopted:** 2026-05-13 by Gunther TM per Yeti directive — "i want one of those folders in every repo".
