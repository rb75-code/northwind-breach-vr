# Cyber Security Escape Room VR — Analysis, Plan & Claude Code Prompts

## 0. Read this first (reality check)

1. **The reference is a point-and-click Unity WebGL game.** You never walk around: one fixed camera on a small office, you click objects to zoom in, rotate them, pick them up, combine them, and open hints. The laptop "browser" (Company Mailbox / Facebook / Company Chat tabs) is a **fake UI inside the game**, not a real web browser. So you do NOT need an embedded real browser. Build a fake browser as a world-space UI. Faster, safer, runs on Quest.
2. **Don't clone their assets, text, posters or code.** It's a commercial product (cybersecurity-escaperoom.com). For a faculty submission, "same structure and mechanics, original/CC0 assets, original puzzle text" is both safe and better marks. Download only CC0 / CC-BY assets and keep a `CREDITS.md`. Do not decompile their build.
3. **30–45 min of full game in a few hours is not achievable at good quality.** What is achievable: a polished **vertical slice** — 1 office room (optionally a 2nd short "server closet"), 7–8 puzzles, 12–15 min gameplay, a real start → tutorial → play → win flow. Show that and describe the rest as roadmap. A tight 12 minutes beats a broken 40.
4. **Why Claude "generates crap" for you:** it can't see the result, and one giant "build everything" prompt makes it guess. Fix = small phases, each ending with a *verification gate* (compiles with 0 errors, play-mode test, screenshot/simulator check) + a `CLAUDE.md` with hard rules.

---

## 1. Video analysis (what's actually in the reference)

**Flow:** Game Information popup ("Start Game") → difficulty (normal / experienced) → tutorial (navigate, zoom, pick up, combine, hints) → play in Fred's office → find secret file → end screen (certificate, stats, end-selfie).

**Story (theirs):** Fred left his office; you exploit his lazy security habits to steal a file. **Yours (blue team):** see §3.

**Room:** small office, beige walls, navy-blue carpet, two warm-wood desks facing each other, grey office chairs, big plant, wall clock/timer, coat on hook, shredder, trash bin, printer, laptop, picture frame, briefcase, drawers, mug, donut, notebook, desk clutter.
**Wall posters:** "PASSWORDS" (6-colour grid: Unique / Change / No Tricks / Don't Count / 2-Factor / Secret), "Clean Desk!", "Only for trash".
**Inspect mode:** zoom into an object, drag to rotate, "Rotate" + "Back" buttons, speech bubble hint at top ("Looks like trash").
**Puzzle items seen:** trash bin (discarded packaging/cups), printer with leftover printed paper, digital picture frame (a pet photo → password clue), laptop (unlocked, "Fred didn't lock his laptop"), mail login (Company Mailbox, wrong-password error), shredder, drawers, briefcase.
**Learning system:** "Learning points (1/25)" panel with Close / Open All; each discovery unlocks a short lesson ("Always lock your workstation…").
**HUD:** top-right yellow 💡 + HINT pill + ⚙ gear; bottom-right curved Back arrow.
**Hints panel:** categories as icons (Room, Inventory, Laptop, Briefcase, Picture Frame, Drawers, Printer, Shredder, Trash); hints adapt to progress.
**Settings:** Quality (Low/Med/High), Language (EN/DE/NL), Difficulty.
**UI style:** white rounded cards, **mint-green header** (≈ #5BF0B0) on the info popup, **pastel-blue header** (≈ #5B9BEF) on Hints/Settings, bold flat poster colours (yellow, purple, blue, orange, green). Stylised semi-realistic 3D, soft ambient light, no harsh shadows, desaturated room + saturated UI.
> Tell Claude Code to sample exact hex values from frames (see Phase 0) instead of trusting these approximations.

---

## 2. VR translation (the design that makes sense)

| Reference (2D) | VR version |
|---|---|
| Click object → zoom | **Grab** the object and pull it to your face (or poke it to "inspect": it floats in front of you, rotate with the hand) |
| Rotate button | Just rotate it in your hand |
| Back button | Release/drop, or a "return" glow button; objects snap back to their spot |
| Inventory | **Wrist inventory** (palm-up menu) or a belt tray; items are grabbable |
| Combine items | Bring one grabbed item near another → snap/highlight → combine |
| HINT 💡 + gear | Wrist menu on the left controller (Hint / Learning points / Settings) |
| Hints panel | World-space card that follows you, ray-interactable |
| Laptop / fake browser | World-space canvas on the laptop screen, **poke** keys or ray-point + trigger; virtual keyboard |
| Learning points panel | World-space board + toast popups when found |
| Tutorial | 2-minute VR tutorial room or in-world prompts (grab, ray, poke, wrist menu) |
| Quality/Language/Difficulty | Settings card (Quality → URP asset swap; difficulty → hint delay / clue strength) |

---

## 3. Original story & puzzle chain (blue team, ~12–15 min)

**Premise:** *"Incident Response, 02:13 AM."* An attacker breached employee **Fred's** office workstation. You're the on-call defender. Contain the breach: find every foothold, lock down the room, and recover the leaked file before the attacker exfiltrates it. Timer on the wall.

1. **Lock the workstation** (laptop left unlocked) → lesson: lock your screen.
2. **Trash/printer evidence** — a printed page and discarded note reveal what the attacker saw → lesson: clean desk, shred sensitive paper.
3. **Shredder puzzle** — reassemble/identify strips, or feed the correct document to the shredder.
4. **Weak password** — poster + picture-frame clue (pet name + year) show how Fred's password was guessed → set a strong password using the poster rules in a keypad/keyboard UI.
5. **Enable 2FA** — find phone/token in drawer, complete a 6-digit code step on the laptop.
6. **Phishing email** — in the fake mailbox, flag the 3 malicious emails of 6 (checking sender, links, urgency).
7. **USB drop** — find a suspicious USB in the briefcase; quarantine it (don't plug it in).
8. **Final: encrypt & secure the file** → unlock the door keypad with the code assembled from clues → escape.

Every solved step unlocks a **Learning Point** (target 8–10 for the slice). Hints escalate: nudge → direction → answer.

---

## 4. Tooling (honest list — verify each exists before relying on it)

- **Unity 6 (LTS), URP, Android build target, OpenXR + Meta XR plugins.**
- **Meta XR All-in-One SDK** (Core + Interaction SDK) → use **Building Blocks**: Camera Rig, Controller Tracking, Grab Interaction, Ray Interaction, Poke Interaction, Hand Grab, Passthrough off.
- **Meta XR Simulator** for testing without the headset (Meta's docs cover enabling it from the Unity menu).
- **A Unity MCP server** so Claude can read the console, create scenes/GameObjects, run play mode and take screenshots. Search GitHub/the MCP registry for "unity mcp" (e.g. CoplayDev/unity-mcp, IvanMurzak/Unity-MCP) and pick the one with *console reading + play-mode + screenshot* tools. In Claude Code, run `/mcp` to confirm it's connected.
- **Skills:** in Claude Code run `/plugin` (marketplace) and search "unity", "csharp", "vr". Also create your own project skill (`.claude/skills/`) from §6 — it's the highest-impact "skill" you can add.
- **Asset sources (free, no watermark, permissive):** Kenney.nl (CC0, office/furniture/UI/audio), Quaternius (CC0), Poly Haven (CC0 models/textures/HDRIs), Poly Pizza, Sketchfab filtered to CC0/CC-BY, Freesound (CC0 filter), Pixabay audio, OpenGameArt, ambientCG (textures). Unity Asset Store free packs also fine.
- Claude Code needs permission for network downloads on **your machine**; run it in the project folder and allow `curl`/`git` + Unity package install.

---

## 5. Timeline for "a few hours" (adjust to your real deadline)

| Time | Goal | Gate |
|---|---|---|
| 0:00–0:20 | Backup + clean project + packages + MCP | 0 compile errors; empty scene runs in Simulator, controllers visible |
| 0:20–0:50 | Rig + interactions test cube (grab/ray/poke) | Grab a cube in Simulator |
| 0:50–1:50 | Office room blockout → real assets, lighting, posters | Screenshot matches reference palette |
| 1:50–3:00 | Puzzles 1–5 + learning points + hints + wrist menu | Play-mode run solves them |
| 3:00–3:40 | Fake browser/laptop (mail, phishing, password) + puzzles 6–8 + win | Full run start→escape |
| 3:40–4:15 | Audio, polish, perf, tutorial, build APK, CREDITS.md | Quest-safe perf (<~100 draw calls spare, baked light), 72/90 fps |
| Remaining | Rehearse the demo, record a backup video | |

**Always keep a recorded run of the Simulator as backup for the faculty demo.**

---

## 6. `CLAUDE.md` (put in the Unity project root)

```md
# Project: Cyber Security Escape Room VR (Unity 6, URP, Meta XR SDK, Quest 3)

## Hard rules
- BEFORE any cleanup: `git init` (if needed), commit, and make a zip backup. Never delete outside /Assets without asking.
- Work in phases. After EACH phase: (1) read the Unity console via MCP, fix ALL errors and warnings you introduced, (2) enter Play Mode and test, (3) take a screenshot, (4) commit.
- Never leave the project non-compiling. If a change breaks compile and can't be fixed in 3 attempts, revert it.
- Use Meta XR Interaction SDK Building Blocks (Camera Rig, Grab, Ray, Poke, Controller Tracking) — do NOT hand-roll XR input.
- Must work in Meta XR Simulator AND Quest 3 (Android, IL2CPP, ARM64, URP mobile settings).
- No placeholder primitives in the final scene. Use downloaded CC0/CC-BY assets; log each in /CREDITS.md (name, author, license, URL).
- Do not copy assets/text from cybersecurity-escaperoom.com. Match style/palette only.
- Code: namespaces, small MonoBehaviours, ScriptableObjects for puzzle/hint/learning-point data, event-driven (no Update polling), no FindObjectOfType in loops, object pooling not needed. Comment sparingly.
- Folder layout: Assets/_Project/{Scenes,Scripts,Prefabs,Materials,Models,Audio,UI,Data}. Remove temp/junk (Library stays git-ignored; add .gitignore).
- Performance: baked lighting, no realtime shadows except 1 directional, GPU instancing/SRP batcher, texture max 2048, target 72 fps.

## Style
- Room: beige walls, navy carpet, warm wood desks, soft ambient light. UI: white rounded cards, mint-green (#5BF0B0) info header, pastel-blue (#5B9BEF) hints/settings header. (Verify from reference frames.)
```

---

## 7. MASTER PROMPT (paste into Claude Code, in the Unity project folder)

> Attach/copy the reference video to the project folder first, e.g. `/Reference/reference.mp4`.

```text
You are the lead Unity VR developer on this project. Read CLAUDE.md first and follow it strictly.

GOAL
Build a polished VR escape-room game "Cyber Security Escape Room VR" in Unity 6 + Meta XR SDK, working in Meta XR Simulator and on Quest 3. It is INSPIRED BY the 2D reference video in /Reference/reference.mp4 (mechanics, structure, art direction, color palette, UI style) but must use original/CC0 assets and original text — do not copy their assets or wording. Players are blue-team defenders doing incident response in a breached office (full design in /Docs/DESIGN.md — create it from the brief below in Phase 0).

PHASE 0 — Analyze (no Unity changes yet)
1. Use ffmpeg to extract a frame every 3s from the reference video into /Reference/frames. View them. Write /Docs/ART_BIBLE.md: exact sampled hex palette (walls, carpet, wood, UI headers, poster colors), lighting mood, object list, UI layout.
2. Write /Docs/DESIGN.md: the VR translation (grab/ray/poke, wrist menu, inventory, hints, learning points, fake in-game browser) and the 8-step puzzle chain: lock workstation; trash/printer evidence; shredder; weak password + picture-frame clue; 2FA; phishing email triage; USB quarantine; final encrypt + door keypad. Target 12–15 min.
3. Write /Docs/ASSETS.md: list every asset needed, with a chosen CC0/CC-BY source (Kenney, Quaternius, Poly Haven, Poly Pizza, ambientCG, Sketchfab CC0, Freesound CC0). Stop and show me the lists for approval ONLY if something is ambiguous; otherwise continue.

PHASE 1 — Safe reset
- Backup (git commit + zip to ../backup.zip). Then delete old scenes/scripts/prefabs/junk, temp files, unused packages, empty folders. Keep installed Meta XR SDK. Add .gitignore. Create folder layout from CLAUDE.md.
- Verify: 0 console errors. Commit.

PHASE 2 — XR foundation
- Create Scene "Main". Add Building Blocks: Camera Rig, Controller Tracking (visible controllers), Grab, Ray, Poke interactions. Add a test cube and a UI panel to verify each interaction in Meta XR Simulator.
- Add a left-wrist menu (Hint / Learning Points / Settings) and a floating inventory tray.
- Verify in Simulator via MCP (play mode + screenshot). Commit.

PHASE 3 — Environment
- Download assets per ASSETS.md into Assets/_Project, set up materials in URP Lit, build the office to match ART_BIBLE (two desks, chairs, plant, shredder, trash bin, printer, laptop, picture frame, briefcase, drawers, coat, posters, wall clock, door keypad). Bake lighting, light probes, reflection probe.
- Make every interactive object a prefab with Grabbable + highlight + audio.
- Verify with screenshots from the player's start position. Commit.

PHASE 4 — Game systems (ScriptableObject-driven)
- GameManager state machine (Intro, Tutorial, Playing, Won), PuzzleStep SO, LearningPoint SO (8–10 entries), HintSystem (3 escalating tiers, per-object), InventoryService, CombineService, Timer, Settings (quality/language EN/DE optional/difficulty).
- World-space UI in the reference style: Game Information card with Start, hints card, learning-points board with toasts, settings card.
- Tutorial: guided grab, ray, poke, wrist menu.

PHASE 5 — Puzzles + fake browser
- Implement the 8 puzzles using the systems above. Laptop screen = world-space canvas "Company Mailbox" with login, inbox of 6 emails (3 phishing), tabs (Mailbox / Chat), a poke-able on-screen keyboard. Password rules enforced from the poster guidance. 2FA code step. USB quarantine. Final door keypad.
- Win screen: stats (time, hints used, learning points) + certificate-style card.

PHASE 6 — Polish & build
- Audio: ambient office hum, UI clicks, grab/drop, success/fail stings, music loop (all CC0, logged in CREDITS.md). Haptics on grab.
- Performance pass for Quest 3. Android build settings (IL2CPP, ARM64, Vulkan/GLES3 per Meta docs), build APK to /Builds.
- Final: run a full playthrough in Play Mode, fix every error/warning, remove temp files, update README with how to run in Simulator and on device.

RULES FOR EVERY PHASE
- Finish a phase fully, run the verification gate, commit, then print a 5-line status. Do not ask questions unless blocked; make reasonable decisions and record them in /Docs/DECISIONS.md.
- If an asset download fails or its license is unclear, pick another source.
- Never claim something works without a console check + play-mode test + screenshot.
Begin with Phase 0.
```

---

## 8. Tips for the demo and for brainstorming with faculty

- **Say** "inspired by an existing 2D serious game; re-designed natively for VR with original assets" — that's the honest story and strong academically.
- Pitch the added value: embodied learning, spatial memory, hand interaction, adaptive hints, learning-point scoring.
- Roadmap slide: red-team mode, more rooms, multiplayer, analytics dashboard, certificates (all visible in the reference's "other features").
- Keep a **fallback**: recorded Simulator video + the APK. Don't debug live.
