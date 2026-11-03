#!/usr/bin/env python3
"""echoes social video renderer: 1080x1920, 30 fps, neon-cyan brand style.

Usage:
  python3 render.py posts.json outdir                 # render every post
  python3 render.py posts.json outdir --only w1-01     # one post
  python3 render.py posts.json outdir --preview w1-01 --times 1.2,6.5,11.0
"""
import argparse, json, math, os, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
BG = np.array([4, 7, 12], np.float32)
CYAN = np.array([64, 236, 255], np.float32)
WHITE = (236, 252, 255)
FONT_DIR = "/usr/share/fonts/opentype/inter/"
F_HEAD = FONT_DIR + "InterDisplay-SemiBold.otf"
F_WORD = FONT_DIR + "InterDisplay-ExtraLight.otf"
F_LIGHT = FONT_DIR + "InterDisplay-Light.otf"

ORB_C = (540, 700)
TEXT_Y = 1270
SCREEN_DUR = 2.5
END_DUR = 3.4


# ---------- static layers ----------
def topo_layer(seed, tw=1400, th=2400):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:th, 0:tw].astype(np.float32)
    f = np.zeros((th, tw), np.float32)
    for _ in range(16):
        cx, cy = rng.uniform(0, tw), rng.uniform(0, th)
        s = rng.uniform(170, 520)
        f += rng.uniform(-1, 1) * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * s * s))
    f += 0.12 * np.sin(xx / 330 + rng.uniform(0, 6)) * np.cos(yy / 290 + rng.uniform(0, 6))
    lv = f * 10
    gy, gx = np.gradient(lv)
    g = np.sqrt(gx * gx + gy * gy) + 1e-4
    d = np.abs(lv - np.round(lv)) / g
    line = np.exp(-(d / 1.15) ** 2)
    glow = np.asarray(Image.fromarray((line * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
    inten = np.clip(line * 0.22 + glow * 0.35, 0, 1)
    rgb = BG[None, None, :] + inten[..., None] * CYAN[None, None, :]
    return rgb.astype(np.float32)


def vignette():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.42) / (H * 0.62)) ** 2)
    return np.clip(1.15 - d * 0.75, 0.25, 1.0)[..., None].astype(np.float32)


def orb_sprite(size=820):
    c = size / 2
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    r = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    core = np.clip(1 - (r - 96) / 6, 0, 1)                  # crisp disc edge at r~96
    inner = np.exp(-(r / 70) ** 2)                            # hot centre
    halo = np.exp(-(r / 150) ** 2) * 0.55 + np.exp(-(r / 300) ** 2) * 0.28
    rim = np.exp(-((r - 96) / 5) ** 2) * 0.9
    edge = np.clip((c - 8 - r) / (c * 0.35), 0, 1) ** 2      # fade to zero before the sprite border
    halo = halo * edge
    cyan = (core * 0.55 + halo + rim)[..., None] * CYAN
    white = (inner * core * 0.9)[..., None] * np.array([235, 255, 255], np.float32)
    return cyan + white


def particle_sprite(s=21):
    c = s // 2
    yy, xx = np.mgrid[0:s, 0:s].astype(np.float32)
    r2 = (xx - c) ** 2 + (yy - c) ** 2
    return (np.exp(-r2 / 3.0) + 0.35 * np.exp(-r2 / 18.0))[..., None] * CYAN


def text_sprite(text, font_path, size, tracking=0, glow=10, glow_strength=0.9, color=WHITE):
    font = ImageFont.truetype(font_path, size)
    widths = [font.getbbox(ch)[2] - font.getbbox(ch)[0] for ch in text] if tracking else None
    if tracking:
        tw = sum(font.getlength(ch) for ch in text) + tracking * (len(text) - 1)
    else:
        tw = font.getlength(text)
    asc, desc = font.getmetrics()
    pad = glow * 3
    w, h = int(tw + pad * 2), int(asc + desc + pad * 2)
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    if tracking:
        x = pad
        for ch in text:
            d.text((x, pad), ch, font=font, fill=255)
            x += font.getlength(ch) + tracking
    else:
        d.text((pad, pad), text, font=font, fill=255)
    m = np.asarray(mask, np.float32) / 255
    gl = np.asarray(mask.filter(ImageFilter.GaussianBlur(glow)), np.float32) / 255 * glow_strength
    a = np.clip(m + gl, 0, 1)
    col = np.array(color, np.float32)
    rgb = m[..., None] * col + gl[..., None] * CYAN          # premultiplied
    return {"rgb": rgb, "a": a, "w": w, "h": h}


def fit_size(lines, font_path, base, max_w=860):
    size = base
    while size > 30:
        f = ImageFont.truetype(font_path, size)
        if max(f.getlength(l) for l in lines) <= max_w:
            return size
        size -= 2
    return size


# ---------- compositing helpers ----------
def add_at(frame, spr, cx, cy, k=1.0):
    h, w = spr.shape[:2]
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    fx0, fy0, fx1, fy1 = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
    if fx0 >= fx1 or fy0 >= fy1:
        return
    frame[fy0:fy1, fx0:fx1] += spr[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0] * k


def over_at(frame, ts, cx, cy, alpha):
    if alpha <= 0.003:
        return
    x0, y0 = int(cx - ts["w"] / 2), int(cy - ts["h"] / 2)
    fx0, fy0 = max(x0, 0), max(y0, 0)
    fx1, fy1 = min(x0 + ts["w"], W), min(y0 + ts["h"], H)
    sa = ts["a"][fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0][..., None] * alpha
    sr = ts["rgb"][fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0] * alpha
    region = frame[fy0:fy1, fx0:fx1]
    frame[fy0:fy1, fx0:fx1] = region * (1 - sa) + sr


def ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


# ---------- one post ----------
class Post:
    def __init__(self, post, seed):
        self.post = post
        rng = np.random.default_rng(seed)
        self.topo = topo_layer(seed)
        self.vig = vignette()
        self.orb = orb_sprite()
        self.psprite = particle_sprite()
        self.np_ = 70
        self.px = rng.uniform(40, W - 40, self.np_)
        self.py = rng.uniform(0, H, self.np_)
        self.pv = rng.uniform(10, 38, self.np_)
        self.pk = rng.uniform(0.25, 0.9, self.np_)
        self.pph = rng.uniform(0, 6.28, self.np_)
        # ripple grid around orb
        self.rr_box = (ORB_C[0] - 540, ORB_C[1] - 620, ORB_C[0] + 540, ORB_C[1] + 620)
        x0, y0, x1, y1 = self.rr_box
        yy, xx = np.mgrid[max(y0, 0):min(y1, H), max(x0, 0):min(x1, W)].astype(np.float32)
        self.rr = np.sqrt((xx - ORB_C[0]) ** 2 + (yy - ORB_C[1]) ** 2)
        self.rr_slice = (slice(max(y0, 0), min(y1, H)), slice(max(x0, 0), min(x1, W)))

        screens = post["screens"]
        self.text_screens = screens[:-1]
        self.sprites = []
        for lines in self.text_screens:
            size = fit_size(lines, F_HEAD, 74)
            self.sprites.append([text_sprite(l, F_HEAD, size) for l in lines])
            self.line_h = int(size * 1.28)
        self.size_lines = [fit_size(l, F_HEAD, 74) for l in self.text_screens]
        word = screens[-1][0]
        self.word = word
        self.letters = [text_sprite(ch, F_WORD, 168, glow=14, glow_strength=1.1) for ch in word]
        font = ImageFont.truetype(F_WORD, 168)
        self.letter_adv = [font.getlength(ch) + 10 for ch in word]
        self.tagline = text_sprite(screens[-1][1], F_LIGHT, 54, tracking=3, glow=8, glow_strength=0.6)
        self.avail = text_sprite("free on iPhone & Android", F_LIGHT, 36, tracking=2, glow=6,
                                 glow_strength=0.5, color=(150, 238, 250))
        self.n_text = len(self.text_screens)
        self.end_start = self.n_text * SCREEN_DUR
        self.duration = self.end_start + END_DUR

    def frame(self, t):
        ox = int(170 + 70 * math.sin(t * 0.33))
        oy = int(230 - t * 14)
        f = self.topo[oy:oy + H, ox:ox + W].copy()
        f *= self.vig

        # ripples (echo rings)
        rings = np.zeros_like(self.rr)
        period, life = 1.25, 2.6
        k0 = int(t // period)
        for k in range(k0 - 3, k0 + 1):
            age = t - k * period
            if 0 <= age <= life:
                p = age / life
                R = 110 + 470 * ease(p)
                w = 3 + 10 * p
                amp = (1 - p) ** 1.6 * 0.55
                rings += np.exp(-((self.rr - R) / w) ** 2) * amp
        f[self.rr_slice] += rings[..., None] * CYAN

        # particles
        for i in range(self.np_):
            y = (self.py[i] - self.pv[i] * t) % H
            x = self.px[i] + 14 * math.sin(t * 0.7 + self.pph[i])
            tw = 0.55 + 0.45 * math.sin(t * 2.1 + self.pph[i] * 3)
            add_at(f, self.psprite, x, y, self.pk[i] * tw)

        # orb with breathing pulse; flare on end card
        pulse = 0.9 + 0.12 * math.sin(t * 2 * math.pi / 2.5)
        if t >= self.end_start:
            e = t - self.end_start
            pulse += 0.45 * math.exp(-e * 2.2)
        add_at(f, self.orb, ORB_C[0], ORB_C[1], pulse)

        # text screens
        if t < self.end_start:
            i = int(t // SCREEN_DUR)
            lt = t - i * SCREEN_DUR
            sprs = self.sprites[i]
            line_h = int(self.size_lines[i] * 1.3)
            n = len(sprs)
            top = TEXT_Y - (n - 1) * line_h / 2
            for j, s in enumerate(sprs):
                d = j * 0.14
                a_in = ease((lt - d) / 0.45)
                a_out = 1 - ease((lt - (SCREEN_DUR - 0.38)) / 0.32)
                a = a_in * a_out
                rise = (1 - ease((lt - d) / 0.55)) * 26
                over_at(f, s, W / 2, top + j * line_h + rise, a)
        else:
            e = t - self.end_start
            total = sum(self.letter_adv) - 10
            x = W / 2 - total / 2
            for j, s in enumerate(self.letters):
                st = 0.15 + j * 0.13
                a = ease((e - st) / 0.25)
                flash = math.exp(-max(e - st, 0) * 5) * 0.9 if e >= st else 0
                cx = x + self.letter_adv[j] / 2 - 5
                over_at(f, s, cx, 1225, a)
                if flash > 0.02:
                    over_at(f, s, cx, 1225, min(flash, 1.0) * 0.6)
                x += self.letter_adv[j]
            over_at(f, self.tagline, W / 2, 1385 + (1 - ease((e - 1.05) / 0.5)) * 18, ease((e - 1.05) / 0.5))
            over_at(f, self.avail, W / 2, 1480, ease((e - 1.5) / 0.5) * 0.95)

        # global fade in / out
        g = min(1.0, t / 0.35) * min(1.0, (self.duration - t) / 0.3)
        f *= max(g, 0)
        return np.clip(f, 0, 255).astype(np.uint8)


# ---------- audio ----------
def make_audio(path, duration, n_text, end_start, seed, sr=48000):
    rng = np.random.default_rng(seed)
    n = int(duration * sr)
    t = np.arange(n) / sr
    out = np.zeros(n, np.float64)
    # airy drone: A2, E3, B3, E4 with slow beating
    for fr, amp in [(110, 0.16), (164.81, 0.11), (246.94, 0.07), (329.63, 0.05)]:
        det = fr * 1.003
        lfo = 0.75 + 0.25 * np.sin(2 * np.pi * t * rng.uniform(0.08, 0.2) + rng.uniform(0, 6))
        out += amp * lfo * (np.sin(2 * np.pi * fr * t) + 0.6 * np.sin(2 * np.pi * det * t + 1))
    env = np.minimum(1, t / 1.2) * np.minimum(1, (duration - t) / 0.6)
    out *= env

    def ping(at, freq, gain, echoes=4, delay=0.32, fb=0.45):
        for k in range(echoes):
            s = at + k * delay
            i0 = int(s * sr)
            if i0 >= n:
                break
            m = min(n - i0, int(2.2 * sr))
            tt = np.arange(m) / sr
            tone = (np.sin(2 * np.pi * freq * tt) + 0.3 * np.sin(2 * np.pi * freq * 2 * tt)) * np.exp(-tt * 3.2)
            att = np.minimum(1, tt / 0.004)
            out[i0:i0 + m] += tone * att * gain * (fb ** k)

    for i in range(n_text):
        ping(i * SCREEN_DUR + 0.05, [880, 987.77, 1108.73, 1318.51][i % 4], 0.18)
    pent = [659.25, 739.99, 880, 987.77, 1108.73, 1318.51, 1479.98]
    for j in range(6):
        ping(end_start + 0.15 + j * 0.13, pent[j % len(pent)], 0.11, echoes=3, delay=0.24, fb=0.4)
    out = out / (np.max(np.abs(out)) + 1e-9) * 0.5
    data = (out * 32767).astype(np.int16)
    stereo = np.stack([data, data], axis=1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(stereo.tobytes())


def render(post, seed, outdir):
    p = Post(post, seed)
    final = os.path.join(outdir, post["video"])
    tmp_v = final[:-4] + ".part-v.mp4"
    tmp_a = final[:-4] + ".part-a.wav"
    tmp_f = final[:-4] + ".part.mp4"
    nframes = int(round(p.duration * FPS))
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
         "-pix_fmt", "yuv420p", tmp_v], stdin=subprocess.PIPE)
    for k in range(nframes):
        proc.stdin.write(p.frame(k / FPS).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        raise SystemExit(f"video encode failed for {post['id']}")
    make_audio(tmp_a, nframes / FPS, p.n_text, p.end_start, seed)
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp_v, "-i", tmp_a, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp_f])
    if r.returncode != 0:
        raise SystemExit(f"mux failed for {post['id']}")
    os.replace(tmp_f, final)
    os.remove(tmp_v)
    os.remove(tmp_a)
    print(f"{post['id']}: {final} ({nframes / FPS:.1f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("posts")
    ap.add_argument("outdir")
    ap.add_argument("--only", default="")
    ap.add_argument("--preview", default="")
    ap.add_argument("--times", default="")
    args = ap.parse_args()
    data = json.load(open(args.posts))
    posts = data["posts"]
    os.makedirs(args.outdir, exist_ok=True)
    for idx, post in enumerate(posts):
        seed = 1000 + idx * 17 + sum(map(ord, post["id"]))
        if args.preview:
            if post["id"] != args.preview:
                continue
            p = Post(post, seed)
            for ts in args.times.split(","):
                t = float(ts)
                Image.fromarray(p.frame(t)).save(os.path.join(args.outdir, f"{post['id']}_t{t:.2f}.png"))
            print("duration", p.duration)
            continue
        if args.only and post["id"] not in args.only.split(","):
            continue
        render(post, seed, args.outdir)


if __name__ == "__main__":
    main()
