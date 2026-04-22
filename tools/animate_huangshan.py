from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path("/workspace")
SRC = ROOT / "images" / "image1170x530cropped.jpg"
OUT_DIR = ROOT / "images" / "huangshan_animation"
FRAMES_DIR = OUT_DIR / "frames"
ENHANCED_STILL = OUT_DIR / "huangshan_enhanced.jpg"

FPS = 18
DURATION = 7
FRAME_COUNT = FPS * DURATION


def ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)


def shift_with_edge(arr: np.ndarray, dx: int, dy: int) -> np.ndarray:
    h, w = arr.shape[:2]
    pad_x = abs(dx) + 2
    pad_y = abs(dy) + 2
    if arr.ndim == 2:
        padded = np.pad(arr, ((pad_y, pad_y), (pad_x, pad_x)), mode="edge")
        return padded[pad_y - dy : pad_y - dy + h, pad_x - dx : pad_x - dx + w]

    padded = np.pad(arr, ((pad_y, pad_y), (pad_x, pad_x), (0, 0)), mode="edge")
    return padded[pad_y - dy : pad_y - dy + h, pad_x - dx : pad_x - dx + w, :]


def to_uint8(arr: np.ndarray) -> np.ndarray:
    return np.clip(arr * 255.0, 0, 255).astype(np.uint8)


def soft_blur(mask: np.ndarray, radius: float) -> np.ndarray:
    img = Image.fromarray((np.clip(mask, 0, 1) * 255).astype(np.uint8), mode="L")
    return np.asarray(img.filter(ImageFilter.GaussianBlur(radius=radius)), dtype=np.float32) / 255.0


def build_masks(base_arr: np.ndarray) -> dict[str, np.ndarray]:
    h, w = base_arr.shape[:2]
    brightness = base_arr.mean(axis=2)
    saturation = base_arr.max(axis=2) - base_arr.min(axis=2)

    yy, xx = np.mgrid[0:h, 0:w]
    y = yy / max(h - 1, 1)
    x = xx / max(w - 1, 1)

    sky_band = np.clip(1.0 - (y / 0.42), 0, 1)
    sky_mask = soft_blur(sky_band, 14)

    cloud_logic = (
        (brightness > 0.58).astype(np.float32)
        * (saturation < 0.22).astype(np.float32)
        * (y > 0.14).astype(np.float32)
        * (y < 0.88).astype(np.float32)
    )
    cloud_mask = soft_blur(cloud_logic, 16)

    cloud_focus = np.exp(-((x - 0.5) ** 2) / 0.16) * np.exp(-((y - 0.56) ** 2) / 0.18)
    cloud_mask = np.clip(cloud_mask * 0.65 + cloud_focus * 0.35, 0, 1)

    valley_blob_1 = np.exp(-(((x - 0.54) ** 2) / 0.02 + ((y - 0.72) ** 2) / 0.015))
    valley_blob_2 = np.exp(-(((x - 0.72) ** 2) / 0.03 + ((y - 0.66) ** 2) / 0.02))
    valley_blob_3 = np.exp(-(((x - 0.35) ** 2) / 0.03 + ((y - 0.70) ** 2) / 0.02))
    mist_mask = soft_blur(np.clip(valley_blob_1 + valley_blob_2 + valley_blob_3, 0, 1), 20)

    sun_x = 0.60
    sun_y = 0.17
    glow = np.exp(-(((x - sun_x) ** 2) / 0.03 + ((y - sun_y) ** 2) / 0.01))
    glow_mask = soft_blur(glow, 12)

    return {
        "sky": sky_mask.astype(np.float32),
        "cloud": cloud_mask.astype(np.float32),
        "mist": mist_mask.astype(np.float32),
        "glow": glow_mask.astype(np.float32),
    }


def enhance_still(src: Image.Image) -> Image.Image:
    img = src.convert("RGB")
    img = ImageEnhance.Color(img).enhance(1.16)
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Brightness(img).enhance(1.03)
    img = ImageEnhance.Sharpness(img).enhance(1.06)

    arr = np.asarray(img, dtype=np.float32) / 255.0
    masks = build_masks(arr)

    # Warm the sunrise and gently lift cloud luminance.
    warm = np.dstack(
        [
            masks["glow"] * 0.26,
            masks["glow"] * 0.16,
            masks["glow"] * 0.07,
        ]
    )
    cool_sky = np.dstack(
        [
            masks["sky"] * 0.02,
            masks["sky"] * 0.05,
            masks["sky"] * 0.10,
        ]
    )
    cloud_lift = np.dstack([masks["cloud"] * 0.05] * 3)

    arr = np.clip(arr + warm + cool_sky + cloud_lift, 0, 1)
    return Image.fromarray(to_uint8(arr), mode="RGB")


def apply_ken_burns(frame: Image.Image, t: float) -> Image.Image:
    w, h = frame.size
    zoom = 1.0 + 0.018 * (1 - math.cos(2 * math.pi * t))
    scaled = frame.resize((int(w * zoom), int(h * zoom)), Image.Resampling.LANCZOS)
    sw, sh = scaled.size

    dx = int((sw - w) / 2 + math.sin(2 * math.pi * t) * 7)
    dy = int((sh - h) / 2 + math.sin(2 * math.pi * t + 0.9) * 4)
    return scaled.crop((dx, dy, dx + w, dy + h))


def render_frames() -> None:
    ensure_dirs()
    src = Image.open(SRC)
    enhanced = enhance_still(src)
    enhanced.save(ENHANCED_STILL, quality=95)

    base = np.asarray(enhanced, dtype=np.float32) / 255.0
    h, w = base.shape[:2]
    masks = build_masks(base)

    cloud_layer = np.asarray(
        enhanced.filter(ImageFilter.GaussianBlur(radius=4)), dtype=np.float32
    ) / 255.0

    yy, xx = np.mgrid[0:h, 0:w]
    x = xx / max(w - 1, 1)
    y = yy / max(h - 1, 1)

    for i in range(FRAME_COUNT):
        t = i / FRAME_COUNT
        frame = base.copy()

        dx1 = int(round(10 * math.sin(2 * math.pi * t)))
        dy1 = int(round(3 * math.cos(2 * math.pi * t)))
        dx2 = int(round(-7 * math.sin(2 * math.pi * t * 1.4 + 0.5)))
        dy2 = int(round(4 * math.sin(2 * math.pi * t * 0.9)))

        cloud1 = shift_with_edge(cloud_layer, dx1, dy1)
        cloud2 = shift_with_edge(cloud_layer, dx2, dy2)

        alpha1 = np.clip(masks["cloud"] * (0.18 + 0.06 * math.sin(2 * math.pi * t)), 0, 1)[
            ..., None
        ]
        alpha2 = np.clip(
            masks["cloud"] * (0.10 + 0.04 * math.cos(2 * math.pi * t * 1.2)),
            0,
            1,
        )[..., None]

        frame = frame * (1 - alpha1) + cloud1 * alpha1
        frame = frame * (1 - alpha2) + cloud2 * alpha2

        # Animated mist rising from valleys.
        mist_shift = np.clip(y - (0.008 * math.sin(2 * math.pi * t * 1.3)), 0, 1)
        mist_wobble = 0.5 + 0.5 * np.sin(2 * math.pi * (x * 1.2 + t))
        mist_strength = np.clip(masks["mist"] * (0.16 + 0.06 * mist_wobble), 0, 1)
        mist_color = np.dstack(
            [
                mist_strength * 1.0,
                mist_strength * 1.0,
                mist_strength * 1.02,
            ]
        )
        frame = np.clip(frame + mist_color * (1 - mist_shift[..., None]) * 0.22, 0, 1)

        # Dawn glow pulse.
        glow_amp = 0.045 + 0.02 * math.sin(2 * math.pi * t)
        glow = np.dstack(
            [
                masks["glow"] * (glow_amp * 1.25),
                masks["glow"] * glow_amp,
                masks["glow"] * (glow_amp * 0.5),
            ]
        )
        frame = np.clip(frame + glow, 0, 1)

        # Gentle sky luminance breathing.
        sky_breath = 0.015 + 0.01 * math.sin(2 * math.pi * t + 0.6)
        frame = np.clip(frame + np.dstack([masks["sky"] * sky_breath] * 3), 0, 1)

        out = Image.fromarray(to_uint8(frame), mode="RGB")
        out = apply_ken_burns(out, t)
        out.save(FRAMES_DIR / f"frame_{i:03d}.png")


if __name__ == "__main__":
    render_frames()
