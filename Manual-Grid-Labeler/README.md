# Grid Challenge Labeler

A single-file, offline tool for hand-labeling image-grid challenges — the kind where you
pick which of *n* candidate tiles matches a reference image.

Open `index.html` in a browser. No install, no server, no build step. **Nothing is uploaded** —
images are read locally and progress is kept in your browser's `localStorage`.

---

## Supported layout

One layout is supported right now:

```
┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│  0   │  1   │  2   │  3   │  4   │  5   │  6   │  7   │   ← candidates, one square row
└──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
┌────────────┐
│ reference  │                                              ← reference, below on the left
└────────────┘
```

* candidates sit in a **single top row** of *n* **equal square** tiles
* tiles are indexed **`0 … n-1`, left to right**
* the **reference** sits below the row, on the left
* tile count is configurable (default `8`)

If your challenge uses a different arrangement, this tool won't index it correctly.

---

## Usage

1. **Name the variant** in the header (e.g. `claw_machine`). It's written into every exported row.
2. **Load one variant at a time.** Drop a folder, or use *Choose folder*.
   Mixing challenge types in one session produces inconsistent labels.
3. **Click the tile** that matches the reference, or press its number key. It auto-advances.
4. **Download labels** to get a `.jsonl`.

### Keyboard

| Key | Action |
| --- | --- |
| `0`–`9` | pick that tile |
| `←` `→` | previous / next image |
| `S` or `Space` | skip |
| `Backspace` | clear this image's label |

**Skip freely.** A skipped image costs nothing; a guessed label teaches a model something false.

---

## Output

One JSON object per line (`<variant>_labels.jsonl`):

```json
{"id":"a1b2c3d4","variant":"claw_machine","guess":3,"n_cand":8,"source":"human"}
```

| field | meaning |
| --- | --- |
| `id` | filename without extension |
| `variant` | what you typed in the header |
| `guess` | **0-based** index of the chosen tile |
| `n_cand` | number of candidate tiles |
| `source` | always `human` |

> `guess` is **0-based**: the leftmost tile is `0`, so `"guess":3` is the **4th** tile.
> Tiles are labeled `0…n-1` on screen to match.

Only labels for the **currently loaded folder** are exported, so separate batches stay separate.
Skipped images are omitted entirely.

---

## Notes

* Progress survives a page reload and is keyed per image id, so you can stop and resume,
  or move between folders without losing work. **Reset** clears it.
* Folder picking uses `webkitdirectory` (Chrome/Edge/Safari). In Firefox, use
  *Choose files* or drag a folder onto the drop zone.
* Supported files: `.png`, `.jpg`, `.jpeg`, `.webp`.
