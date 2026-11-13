#!/usr/bin/env python3
"""Pull skills from the repos listed in skills.sources.json into skills/<pack>/<name>/.

    python3 scripts/sync_skills.py                 # sync every source
    python3 scripts/sync_skills.py --only emilkowalski-skills
    python3 scripts/sync_skills.py --sync-forks    # first update your forks from their upstream (needs `gh auth login`)
    python3 scripts/sync_skills.py --prune         # also delete skills that disappeared upstream

What it does for each source:
  1. shallow, sparse clone of the repo
  2. finds skills: every sub-folder of each "roots" folder that has a SKILL.md (so NEW upstream skills are
     picked up with no edit here), plus the explicit "skills" entries
  3. checks the repo's licence file against the allow-list. No licence, or not on the list: the skill is skipped
  4. copies the skill, adds the licence/notice files, skips pictures, fonts, audio, video and files over the size cap
  5. writes skills/LOCK.json (commit, licence, content hash), skills/CATALOG.md, and skills/<pack>/INDEX.tsv

It never commits. Run `git diff` afterwards and READ it: you are pulling instructions and scripts written by
other people into your agents.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "skills.sources.json"
SKILLS = ROOT / "skills"
LOCK = SKILLS / "LOCK.json"

BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico", ".bmp", ".tif", ".tiff",
              ".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".mov", ".webm", ".mkv",
              ".woff", ".woff2", ".ttf", ".otf", ".eot", ".zip", ".gz", ".tgz", ".7z", ".pdf"}
LICENCE_FILE = re.compile(r"^(licen[sc]e|copying)([-._].*)?$", re.I)
NOTICE_FILE = re.compile(r"^notice([-._].*)?$", re.I)
HINTS = [re.compile(p, re.I) for p in (
    r"curl[^\n|]*\|\s*(sudo\s+)?(ba)?sh", r"wget[^\n|]*\|\s*(sudo\s+)?(ba)?sh",
    r"rm\s+-rf\s+(/|~|\$HOME)")]


def say(msg):
    print(msg, flush=True)


def run(cmd, cwd=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def detect_licences(text):
    t = text
    found = set()
    if "Apache License" in t and "Version 2.0" in t:
        found.add("Apache-2.0")
    if "Permission is hereby granted, free of charge, to any person obtaining a copy" in t:
        found.add("MIT")
    if "ISC License" in t or "with or without fee is hereby granted" in t:
        found.add("ISC")
    if "Redistribution and use in source and binary forms" in t:
        found.add("BSD")
    if "free and unencumbered software released into the public domain" in t:
        found.add("Unlicense")
    if "GNU AFFERO" in t.upper():
        found.add("AGPL")
    elif "GNU GENERAL PUBLIC LICENSE" in t.upper():
        found.add("GPL")
    if "Mozilla Public License" in t:
        found.add("MPL")
    if "Creative Commons" in t:
        found.add("CC")
    # a custom licence that merely borrows a sentence from a standard one is not that standard licence
    if re.search(r"company license|eligib(le|ility)|you are not allowed|non-commercial use only", t, re.I):
        found = {"Custom"}
    return found


def licence_files(folder):
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_file() and LICENCE_FILE.match(p.name))


def notice_files(folder):
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_file() and NOTICE_FILE.match(p.name))


def frontmatter(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\r?\n(.*?)\r?\n---", text, re.S)
    fm, cur = {}, None
    if not m:
        return fm
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if km and not line.startswith((" ", "\t")):
            cur = km.group(1)
            fm[cur] = km.group(2).strip()
        elif cur and line.strip():
            fm[cur] += " " + line.strip()
    for k, v in fm.items():
        v = re.sub(r"^[>|][-+]?\s*", "", v.strip()).strip().strip("\"'")
        fm[k] = re.sub(r"\s+", " ", v)
    return fm


def tree_hash(folder):
    h = hashlib.sha256()
    for p in sorted(folder.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(folder)).encode())
            h.update(p.read_bytes())
    return h.hexdigest()[:16]


def clone(repo, dest, sparse_paths):
    url = f"https://github.com/{repo}.git"
    cmd = ["git", "clone", "--depth", "1", "--filter=blob:none", "--quiet"]
    if sparse_paths is not None:
        cmd.append("--sparse")
    r = run(cmd + [url, str(dest)])
    if r.returncode != 0:
        return False, r.stderr.strip()[:200]
    if sparse_paths:
        r = run(["git", "sparse-checkout", "set", "--cone", *sparse_paths], cwd=dest)
        if r.returncode != 0:
            return False, r.stderr.strip()[:200]
    return True, run(["git", "rev-parse", "--short", "HEAD"], cwd=dest).stdout.strip()


def sparse_paths_for(src):
    if src.get("sparse") is False:
        return None
    paths = []
    for r in src.get("roots", []):
        if r != ".":
            paths.append(r)
    for s in src.get("skills", []):
        if s["path"] == ".":
            return None
        paths.append(s["path"])
    return paths if paths and "." not in src.get("roots", []) else None


def discover(src, repo_dir):
    found = {}
    for root in src.get("roots", []):
        base = (repo_dir / root).resolve()
        if not base.is_dir():
            say(f"   ! folder not found in repo: {root}")
            continue
        for d in sorted(base.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").is_file():
                found[d.name] = {"dir": d, "include": None, "pack": src["pack"], "path": str(d.relative_to(repo_dir))}
    for s in src.get("skills", []):
        d = (repo_dir / s["path"]).resolve()
        if (d / "SKILL.md").is_file():
            found[s["name"]] = {"dir": d, "include": s.get("include"), "pack": s.get("pack", src["pack"]),
                                "path": s["path"]}
        else:
            say(f"   ! no SKILL.md at {s['path']}")
    for ex in src.get("exclude", []):
        found.pop(ex, None)
    return found


def copy_skill(src_dir, include, dest, max_bytes, keep_binaries):
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    omitted = []
    for p in sorted(src_dir.rglob("*")):
        rel = p.relative_to(src_dir)
        if ".git" in rel.parts or p.is_dir():
            continue
        if include and rel.parts[0] not in include:
            continue
        if p.is_symlink():
            omitted.append(f"{rel} (symlink)")
        elif p.suffix.lower() in BINARY_EXT and not keep_binaries:
            omitted.append(str(rel))
        elif p.stat().st_size > max_bytes:
            omitted.append(f"{rel} (over size cap)")
        else:
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
    return omitted


def scan_hints(folder):
    hits = []
    for p in sorted(folder.rglob("*")):
        if p.is_file() and p.suffix.lower() in {".md", ".txt", ".sh", ".py", ".js", ".json", ".yml", ".yaml", ""}:
            if p.stat().st_size > 2_000_000:
                continue
            for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if any(h.search(line) for h in HINTS):
                    hits.append(f"{p.relative_to(folder)}:{n}: {line.strip()[:110]}")
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="sync one source id")
    ap.add_argument("--sync-forks", action="store_true", help="run `gh repo sync` on your forks first")
    ap.add_argument("--prune", action="store_true", help="delete skills that no longer exist upstream")
    args = ap.parse_args()

    cfg = json.loads(MANIFEST.read_text())
    allowed = set(cfg["allowed_licences"])
    max_bytes = cfg.get("max_file_kb", 2048) * 1024
    lock = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    seen_this_run, names_taken = set(), {}
    for key, v in lock.items():
        names_taken[v["name"]] = key
    report = {"added": [], "changed": [], "same": [], "skipped": [], "removed": []}
    tmp = Path(tempfile.mkdtemp(prefix="disciples-sync-"))

    try:
        for src in cfg["sources"]:
            if args.only and src["id"] != args.only:
                continue
            say(f"\n== {src['id']}  ({src['repo']})")
            if args.sync_forks and src.get("fork"):
                r = run(["gh", "repo", "sync", src["repo"]]) if shutil.which("gh") else None
                say("   fork sync: " + ("gh not installed, skipped" if r is None else (r.stdout.strip() or r.stderr.strip())[:120]))
            repo_dir = tmp / src["id"]
            ok, info = clone(src["repo"], repo_dir, sparse_paths_for(src))
            if not ok:
                say(f"   ! could not clone: {info}")
                report["skipped"].append(f"{src['id']} (clone failed)")
                continue
            commit = info
            repo_dir = repo_dir.resolve()
            found = discover(src, repo_dir)
            if not found:
                say("   no skills found")
            root_lic = licence_files(repo_dir)
            root_notice = notice_files(repo_dir)
            for name, s in sorted(found.items()):
                key = f"{s['pack']}/{name}"
                seen_this_run.add(key)
                lic_files = licence_files(s["dir"]) or root_lic
                detected = set()
                for lf in lic_files:
                    detected |= detect_licences(lf.read_text(encoding="utf-8", errors="replace"))
                expected = src.get("licence")
                if not lic_files:
                    say(f"   - {name}: SKIPPED, no licence file (link only: https://github.com/{src['repo']})")
                    report["skipped"].append(f"{key} (no licence)")
                    continue
                if not (detected & allowed) or (expected and expected not in detected):
                    say(f"   - {name}: SKIPPED, licence {sorted(detected) or 'not recognised'} "
                        f"is not on the allow-list (link only: https://github.com/{src['repo']})")
                    report["skipped"].append(f"{key} (licence {sorted(detected) or 'unknown'})")
                    continue
                if names_taken.get(name, key) != key:
                    say(f"   - {name}: SKIPPED, same name already used by {names_taken[name]}")
                    report["skipped"].append(f"{key} (name clash)")
                    continue
                dest = SKILLS / s["pack"] / name
                omitted = copy_skill(s["dir"], s["include"], dest, max_bytes, src.get("keep_binaries", False))
                if not any(LICENCE_FILE.match(p.name) for p in dest.iterdir() if p.is_file()):
                    for i, lf in enumerate(lic_files):
                        shutil.copy2(lf, dest / ("LICENSE" if i == 0 else lf.name))
                for nf in root_notice:
                    if not (dest / nf.name).exists():
                        shutil.copy2(nf, dest / nf.name)
                fm = frontmatter(dest / "SKILL.md")
                digest = tree_hash(dest)
                old = lock.get(key)
                entry = {"name": name, "pack": s["pack"], "source": src["id"], "repo": src["repo"],
                         "path": s["path"], "commit": commit, "licence": sorted(detected & allowed),
                         "hash": digest, "omitted": len(omitted),
                         "description": fm.get("description", "")}
                lock[key] = entry
                names_taken[name] = key
                if old is None:
                    status = "added"
                elif old.get("hash") != digest:
                    status = "changed"
                else:
                    status = "same"
                report[status].append(key)
                extra = f", {len(omitted)} media/large files left out" if omitted else ""
                say(f"   - {name}: {status.upper()} ({'/'.join(entry['licence'])}{extra})")
                if status in ("added", "changed"):
                    for hit in scan_hints(dest)[:5]:
                        say(f"       ? review: {hit}")
            # skills we knew from this source that are gone upstream
            for key, v in list(lock.items()):
                if v["source"] == src["id"] and key not in seen_this_run:
                    report["removed"].append(key)
                    if args.prune:
                        shutil.rmtree(SKILLS / key, ignore_errors=True)
                        del lock[key]
                        say(f"   - {v['name']}: REMOVED (gone upstream)")
                    else:
                        say(f"   - {v['name']}: not found upstream this time (kept; use --prune to delete)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    SKILLS.mkdir(exist_ok=True)
    LOCK.write_text(json.dumps(dict(sorted(lock.items())), indent=2, ensure_ascii=False) + "\n")

    # one TSV per pack: name <TAB> description (the installer turns these into INDEX.md)
    by_pack = {}
    for key, v in sorted(lock.items()):
        by_pack.setdefault(v["pack"], []).append(v)
    for pack, items in by_pack.items():
        rows = []
        for v in items:
            desc = (v["description"] or "(no description)").replace("\t", " ").replace("|", "/")
            rows.append(f"{v['name']}\t{desc[:240]}")
        (SKILLS / pack / "INDEX.tsv").write_text("\n".join(rows) + "\n")

    lines = ["# Skill catalog", "", "Generated by `scripts/sync_skills.py`. Do not edit by hand.", "",
             "| Pack | Skill | From | Licence | Commit | Media left out |", "|---|---|---|---|---|---|"]
    for key, v in sorted(lock.items()):
        lines.append(f"| {v['pack']} | {v['name']} | [{v['repo']}](https://github.com/{v['repo']}) | "
                     f"{'/'.join(v['licence'])} | {v['commit']} | {v['omitted']} |")
    (SKILLS / "CATALOG.md").write_text("\n".join(lines) + "\n")

    say("\n== Summary")
    for k in ("added", "changed", "same", "skipped", "removed"):
        say(f"{k:8} {len(report[k])}" + (f"   {', '.join(report[k][:12])}{' ...' if len(report[k]) > 12 else ''}" if report[k] else ""))
    say("\nNext: run `git diff --stat` and read what changed before you commit.")


if __name__ == "__main__":
    sys.exit(main())
