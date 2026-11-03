#!/usr/bin/env python3
"""echoes reels v2 — real app footage + question hook, in the app's own look
(dark navy, amber/orange, cream text). 1080x1920, 30 fps.

Each post in the JSON has:
  "screens": [[hook lines...], [lines...], ...]          (no end card entry needed)
  "shots":   [[shot, ...], [shot, ...], ...]             one list per screen
  shot = {"clip": "ar_reflection", "from": 0.0, "dur": 2.6, "speed": 1.0}
       | {"still": "map_2d", "dur": 2.6, "zoom": [1.0, 1.08], "pan": [0, -30]}
Assets live in assets/clips and assets/stills (see assets/library.json).
The hook (screen 0) is on screen from frame 0. The video ends on assets/clips/end_card.mp4.

  python3 render2.py week1_posts.json videos [--only w1-01] [--preview w1-01 --times 0,4]
"""
import argparse, json, math, os, subprocess, wave
import numpy as np
from PIL import Image, ImageFilter, ImageFont, ImageDraw

W, H, FPS = 1080, 1920, 30
HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.join(HERE, "assets", "clips")
STILLS = os.path.join(HERE, "assets", "stills")
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"
CREAM = np.array([255, 244, 230], np.float32)
AMBER = np.array([247, 168, 38], np.float32)
NAVY = np.array([14, 19, 28], np.float32)
HOOK_DUR, SCREEN_DUR, END_DUR = 3.0, 2.6, 2.5
TEXT_CY = 560


# ---------- text ----------
def fit(lines, base, max_w=930):
    s = base
    while s > 40:
        f = ImageFont.truetype(FONT, s)
        if max(f.getlength(l) for l in lines) <= max_w:
            return s
        s -= 2
    return s


def line_sprite(text, size, color):
    font = ImageFont.truetype(FONT, size)
    tw = font.getlength(text)
    asc, desc = font.getmetrics()
    pad = 40
    w, h = int(tw + 2 * pad), int(asc + desc + 2 * pad)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text((pad, pad), text, font=font, fill=255)
    m = np.asarray(mask, np.float32) / 255
    sh = np.asarray(mask.filter(ImageFilter.GaussianBlur(16)), np.float32) / 255
    sh = np.roll(sh, 5, axis=0) * 0.85
    a = np.clip(m + sh * (1 - m), 0, 1)
    rgb = m[..., None] * color                      # premultiplied; shadow is black
    return {"rgb": rgb, "a": a, "w": w, "h": h}


def screen_sprites(lines, hook):
    size = fit(lines, 96 if hook else 80)
    out = []
    for i, l in enumerate(lines):
        col = AMBER if i == len(lines) - 1 else CREAM
        out.append(line_sprite(l, size, col))
    return out, int(size * 1.22)


def over(frame, s, cx, cy, alpha):
    if alpha <= 0.004:
        return
    x0, y0 = int(cx - s["w"] / 2), int(cy - s["h"] / 2)
    fx0, fy0, fx1, fy1 = max(x0, 0), max(y0, 0), min(x0 + s["w"], W), min(y0 + s["h"], H)
    a = s["a"][fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0][..., None] * alpha
    r = s["rgb"][fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0] * alpha
    frame[fy0:fy1, fx0:fx1] = frame[fy0:fy1, fx0:fx1] * (1 - a) + r


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


SCRIM = (np.clip(1 - np.arange(1100) / 1100, 0, 1) ** 1.4 * 0.82)[:, None, None].astype(np.float32)


# ---------- footage ----------
def clip_frames(name, start, n, speed=1.0):
    path = os.path.join(CLIPS, name + ".mp4")
    src_dur = n / FPS * speed + 0.1
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", path, "-t", f"{src_dur:.3f}",
           "-vf", f"setpts=PTS/{speed},fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    raw = subprocess.run(cmd, capture_output=True).stdout
    fs = len(raw) // (W * H * 3)
    arr = np.frombuffer(raw[:fs * W * H * 3], np.uint8).reshape(fs, H, W, 3)
    if fs == 0:
        raise SystemExit(f"no frames from {name} @ {start}")
    for k in range(n):
        yield arr[min(k, fs - 1)].astype(np.float32)


def still_frames(name, n, zoom=(1.0, 1.08), pan=(0, 0)):
    im = Image.open(os.path.join(STILLS, name + ".jpg")).convert("RGB")
    iw, ih = im.size
    for k in range(n):
        p = k / max(n - 1, 1)
        z = zoom[0] + (zoom[1] - zoom[0]) * p
        cw, ch = iw / z, ih / z
        cx = iw / 2 + pan[0] * p * (iw / W)
        cy = ih / 2 + pan[1] * p * (ih / H)
        cx = min(max(cx, cw / 2), iw - cw / 2)
        cy = min(max(cy, ch / 2), ih - ch / 2)
        box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
        yield np.asarray(im.resize((W, H), Image.BILINEAR, box=box), np.float32)


def shot_frames(shot):
    n = int(round(shot["dur"] * FPS))
    if "clip" in shot:
        return clip_frames(shot["clip"], shot.get("from", 0.0), n, shot.get("speed", 1.0))
    return still_frames(shot["still"], n, shot.get("zoom", (1.0, 1.08)), shot.get("pan", (0, 0)))


# ---------- audio ----------
def make_audio(path, duration, cuts, end_start, seed, sr=48000):
    rng = np.random.default_rng(seed)
    n = int(duration * sr)
    t = np.arange(n) / sr
    out = np.zeros(n)
    for fr, amp in [(110.0, 0.15), (164.81, 0.10), (220.0, 0.07), (277.18, 0.05), (329.63, 0.035)]:
        lfo = 0.78 + 0.22 * np.sin(2 * np.pi * t * rng.uniform(0.1, 0.25) + rng.uniform(0, 6))
        out += amp * lfo * (np.sin(2 * np.pi * fr * t) + 0.5 * np.sin(2 * np.pi * fr * 1.004 * t + 1))
    out *= np.minimum(1, t / 0.08) * np.minimum(1, (duration - t) / 0.5)

    def ping(at, f, g, echoes=3, delay=0.28, fb=0.42):
        for k in range(echoes):
            i0 = int((at + k * delay) * sr)
            if i0 >= n:
                return
            m = min(n - i0, int(1.8 * sr))
            tt = np.arange(m) / sr
            tone = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 3.5)
            out[i0:i0 + m] += tone * np.minimum(1, tt / 0.004) * g * fb ** k

    notes = [659.25, 739.99, 830.61, 987.77, 1108.73]
    for i, c in enumerate(cuts):
        ping(c, notes[i % len(notes)], 0.2 if i == 0 else 0.15)
    for j, f in enumerate([880.0, 1108.73, 1318.51]):
        ping(end_start + 0.1 + j * 0.12, f, 0.12, echoes=2)
    out = out / (np.abs(out).max() + 1e-9) * 0.5
    d = (out * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(np.stack([d, d], 1).tobytes())


# ---------- a post ----------
def plan(post):
    screens, shots = post["screens"], post["shots"]
    if screens and screens[-1][0] == "echoes":            # tolerate v1 posts that list the end card
        screens = screens[:-1]
    assert len(screens) == len(shots), f"{post['id']}: screens/shots mismatch"
    durs = [HOOK_DUR] + [SCREEN_DUR] * (len(screens) - 1)
    for i, (d, ss) in enumerate(zip(durs, shots)):
        tot = sum(s["dur"] for s in ss)
        assert abs(tot - d) < 0.02, f"{post['id']} screen {i}: shots add to {tot}, need {d}"
    return screens, shots, durs


def frames(post):
    screens, shots, durs = plan(post)
    for i, (lines, ss, dur) in enumerate(zip(screens, shots, durs)):
        sprites, lh = screen_sprites(lines, hook=(i == 0))
        top = TEXT_CY - (len(sprites) - 1) * lh / 2
        k = 0
        for shot in ss:
            for f in shot_frames(shot):
                lt = k / FPS
                f[:1100] = f[:1100] * (1 - SCRIM) + NAVY * SCRIM
                for j, s in enumerate(sprites):
                    if i == 0:
                        a, dy = 1.0, 0.0                       # hook: readable at frame 0
                    else:
                        a = ease((lt - j * 0.08) / 0.18)
                        dy = (1 - ease((lt - j * 0.08) / 0.25)) * 22
                    over(f, s, W / 2, top + j * lh + dy, a)
                yield np.clip(f, 0, 255).astype(np.uint8)
                k += 1
    for f in clip_frames("end_card", 0.0, int(round(END_DUR * FPS))):
        yield f.astype(np.uint8)


def render(post, seed, outdir):
    screens, shots, durs = plan(post)
    final = os.path.join(outdir, post["video"])
    tv, ta, tf = final[:-4] + ".part-v.mp4", final[:-4] + ".part-a.wav", final[:-4] + ".part.mp4"
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "18", "-pix_fmt", "yuv420p", tv], stdin=subprocess.PIPE)
    n = 0
    for fr in frames(post):
        proc.stdin.write(fr.tobytes()); n += 1
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit("encode failed")
    cuts = [sum(durs[:i]) for i in range(len(durs))]
    make_audio(ta, n / FPS, cuts, sum(durs), seed)
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tv, "-i", ta, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tf])
    if r.returncode:
        raise SystemExit("mux failed")
    os.replace(tf, final); os.remove(tv); os.remove(ta)
    print(f"{post['id']}: {final} ({n / FPS:.1f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("posts"); ap.add_argument("outdir")
    ap.add_argument("--only", default=""); ap.add_argument("--preview", default=""); ap.add_argument("--times", default="0")
    a = ap.parse_args()
    d = json.load(open(a.posts))
    os.makedirs(a.outdir, exist_ok=True)
    for idx, post in enumerate(d["posts"]):
        seed = 7000 + idx
        if a.preview:
            if post["id"] != a.preview:
                continue
            want = sorted(int(round(float(t) * FPS)) for t in a.times.split(","))
            for k, fr in enumerate(frames(post)):
                if k in want:
                    Image.fromarray(fr).save(os.path.join(a.outdir, f"{post['id']}_f{k:04d}.png"))
                if k >= want[-1]:
                    break
            continue
        if a.only and post["id"] not in a.only.split(","):
            continue
        render(post, seed, a.outdir)


if __name__ == "__main__":
    main()
