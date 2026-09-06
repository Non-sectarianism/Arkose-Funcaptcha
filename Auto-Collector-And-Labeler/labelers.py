"""Pluggable labelers: pick a candidate index for a challenge image.

The image is a composite: a top row of `n_cand` square candidate tiles (indexed
0..n_cand-1, left to right) with a reference below on the left. A labeler returns
the index it believes matches the reference.

  dino        DINOv2-small embedding nearest-neighbour  (free, CPU, no API key)
  openrouter  a vision LLM via OpenRouter               (needs OPENROUTER_API_KEY)
  random      uniform random                            (baseline / smoke test)

The labeler is only a *bootstrap* — the collector submits its guess to Arkose and
keeps the verdict, so even a weak labeler yields Arkose-verified training data.
Train your own model on the collected data, then plug it in here.
"""
import io, os, re, json, base64, random, urllib.request, urllib.error


# ---------------------------------------------------------------- DINOv2
_dino = {"m": None, "pre": None}

def _load_dino():
    if _dino["m"] is None:
        import torch, torchvision.transforms as T
        m = torch.hub.load("facebookresearch/dinov2", "dinov2_vits14", verbose=False); m.eval()
        _dino["m"] = m
        _dino["pre"] = T.Compose([
            T.Resize(224), T.CenterCrop(224), T.ToTensor(),
            T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    return _dino["m"], _dino["pre"]

def dino_label(img_bytes, n_cand):
    """Candidate whose DINOv2 embedding is nearest the reference. Falls back to random."""
    try:
        import torch, torch.nn.functional as F
        from PIL import Image, ImageChops
        m, pre = _load_dino()
        im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        W, H = im.size; tw = W // max(1, n_cand)
        cands = [im.crop((i * tw, 0, (i + 1) * tw, tw)) for i in range(n_cand)]
        ref = im.crop((0, tw, min(int(tw * 1.5), W), H))
        bg = Image.new(ref.mode, ref.size, (0, 0, 0))
        bbox = ImageChops.difference(ref, bg).getbbox()
        if bbox: ref = ref.crop(bbox)
        ts = torch.stack([pre(x) for x in [ref] + cands])
        with torch.no_grad():
            emb = F.normalize(m(ts), dim=1)
        return int((emb[1:] @ emb[0]).argmax())
    except Exception:
        return random.randrange(n_cand)


# ---------------------------------------------------------------- OpenRouter (optional)
def _or_prompt(n, instruction=""):
    task = f'The challenge instruction says: "{instruction}"\n' if instruction else ""
    return (f"Image-grid matching puzzle. {task}"
            f"BOTTOM-LEFT: a small REFERENCE image. TOP row: {n} CANDIDATE tiles, indexed 0 to {n-1} "
            f"left-to-right. Pick the ONE candidate that matches the reference per the instruction. "
            f"Reply with ONLY the single index digit (0 to {n-1}). No other text.")

def openrouter_label(img_bytes, n_cand, instruction=""):
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    model = os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash")
    if not key:
        return random.randrange(n_cand)
    b64 = base64.b64encode(img_bytes).decode()
    body = json.dumps({"model": model, "max_tokens": 2000, "temperature": 0,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": _or_prompt(n_cand, instruction)},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}}]}]}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=40))
        txt = (r.get("choices", [{}])[0].get("message", {}) or {}).get("content", "") or ""
        digs = [int(d) for d in re.findall(r"[0-9]", txt) if int(d) < n_cand]
        return digs[-1] if digs else random.randrange(n_cand)
    except Exception:
        return random.randrange(n_cand)


# ---------------------------------------------------------------- dispatch
def get_labeler(name):
    if name == "dino":
        return lambda img, n, instr="": dino_label(img, n)
    if name == "openrouter":
        return lambda img, n, instr="": openrouter_label(img, n, instr)
    if name == "random":
        return lambda img, n, instr="": random.randrange(n)
    raise SystemExit(f"unknown labeler '{name}'. Available: dino, openrouter, random")

def preload(name):
    if name == "dino":
        _load_dino()
