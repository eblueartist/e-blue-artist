"""One base image → 7 vertical crops → style filter each → seamless composite."""

from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
BASE_PATH = ASSETS / "lighthouse-base.png"
OUTPUT_PATH = ASSETS / "lighthouse-slices.png"
SLICES = 7
TARGET_WIDTH = 1400


def load_base() -> Image.Image:
    img = Image.open(BASE_PATH).convert("RGB")
    ratio = TARGET_WIDTH / img.width
    size = (TARGET_WIDTH, int(img.height * ratio))
    return img.resize(size, Image.Resampling.LANCZOS)


def pencil_sketch(img: Image.Image) -> Image.Image:
    """Fine pencil — pale lines on white."""
    gray = ImageEnhance.Brightness(img.convert("L")).enhance(1.45)
    lines = gray.filter(ImageFilter.CONTOUR)
    lines = ImageEnhance.Contrast(lines).enhance(0.45)
    paper = Image.new("RGB", img.size, "#fafaf8")
    stroke = ImageOps.colorize(lines, "#fafaf8", "#9aabb8")
    return Image.blend(paper, stroke, 0.32)


def ink_drawing(img: Image.Image) -> Image.Image:
    """Pen and ink — defined black lines on cream."""
    gray = img.convert("L")
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = ImageEnhance.Contrast(edges).enhance(3.5)
    edges = edges.filter(ImageFilter.SHARPEN)
    line_mask = edges.point(lambda x: 255 if x > 68 else 0)
    paper = Image.new("RGB", img.size, "#f6f2eb")
    lines = Image.new("RGB", img.size, "#12151c")
    return Image.composite(lines, paper, line_mask)


def charcoal(img: Image.Image) -> Image.Image:
    """Charcoal — moody dark cliff, heavy grain."""
    gray = img.convert("L")
    dark = ImageEnhance.Brightness(gray).enhance(0.38)
    dark = ImageEnhance.Contrast(dark).enhance(3.2)
    noise = Image.effect_noise(img.size, 55).convert("L")
    mixed = ImageChops.overlay(dark, noise)
    return ImageOps.colorize(mixed, "#040408", "#a8a094")


def watercolor(img: Image.Image) -> Image.Image:
    """Watercolour — soft translucent washes."""
    wash = img.filter(ImageFilter.GaussianBlur(radius=6))
    wash = wash.filter(ImageFilter.SMOOTH_MORE)
    wash = ImageEnhance.Color(wash).enhance(1.15)
    wash = ImageEnhance.Brightness(wash).enhance(1.14)
    return Image.blend(img, wash, 0.85)


def gouache(img: Image.Image) -> Image.Image:
    """Clean flat colour — crisp lighthouse, solid sky."""
    sharp = img.filter(ImageFilter.SHARPEN)
    sharp = ImageEnhance.Color(sharp).enhance(1.55)
    sharp = ImageEnhance.Contrast(sharp).enhance(1.3)
    flat = sharp.quantize(colors=24).convert("RGB")
    return Image.blend(sharp, flat, 0.45)


def pastel(img: Image.Image) -> Image.Image:
    """Pastel — grainy warm strokes on coast."""
    soft = img.filter(ImageFilter.GaussianBlur(radius=1.2))
    soft = ImageEnhance.Brightness(soft).enhance(1.22)
    soft = ImageEnhance.Color(soft).enhance(1.08)
    noise = Image.effect_noise(img.size, 28).convert("L")
    grain = Image.merge("RGB", (noise, noise, noise))
    textured = ImageChops.soft_light(soft, grain)
    return Image.blend(soft, textured, 0.55)


def acrylic(img: Image.Image) -> Image.Image:
    """Oil impasto — thick strokes, vivid sea and sky."""
    vivid = ImageEnhance.Color(img).enhance(1.85)
    vivid = ImageEnhance.Contrast(vivid).enhance(1.55)
    vivid = ImageEnhance.Brightness(vivid).enhance(1.12)
    texture = img.filter(ImageFilter.EMBOSS)
    painted = Image.blend(vivid, texture.convert("RGB"), 0.28)
    return painted.filter(ImageFilter.SHARPEN)


TECHNIQUES = [
    pencil_sketch,
    ink_drawing,
    charcoal,
    watercolor,
    gouache,
    pastel,
    acrylic,
]


def split_and_style(base: Image.Image) -> Image.Image:
    w, h = base.size
    slice_w = w // SLICES
    styled: list[Image.Image] = []

    for i, apply_filter in enumerate(TECHNIQUES):
        left = i * slice_w
        right = w if i == SLICES - 1 else (i + 1) * slice_w
        crop = base.crop((left, 0, right, h))
        styled.append(apply_filter(crop))

    composite = Image.new("RGB", (w, h))
    x = 0
    for part in styled:
        composite.paste(part, (x, 0))
        x += part.width

    return composite


def main() -> None:
    if not BASE_PATH.exists():
        raise FileNotFoundError(f"Base image not found: {BASE_PATH}")

    base = load_base()
    ASSETS.mkdir(parents=True, exist_ok=True)
    composite = split_and_style(base)
    composite.save(OUTPUT_PATH, quality=93)
    print(f"Saved {OUTPUT_PATH} ({composite.width}x{composite.height})")


if __name__ == "__main__":
    main()
