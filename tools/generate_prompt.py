#!/usr/bin/env python3
"""Compose Donut metaphor-meme creative briefs + image prompts from the catalog."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog"
TEMPLATE = ROOT / "prompts" / "templates" / "classic_hijack.md"

INSERT_INSTRUCTIONS = {
    "object_in_hands": "She cradles a glazed donut ring in her hands instead of empty lap.",
    "between_hands": "Between the almost-touching hands floats a glazed donut ring, the spark of the gesture.",
    "creature_body_or_held_object": "The surreal creature wears or carries a glazed donut ring as its impossible center of gravity.",
    "oversized_center": "An oversized glazed donut ring dominates the ordinary room like Magritte's giant apple.",
    "traded_object": "Whatever was being traded on the tables is now identical glazed donut rings.",
    "center_fetish_object": "At the compositional center sits one glazed donut ring as the object of frenzy.",
    "head_or_held_object": "Replace the figure's head or the held trophy with a glazed donut ring.",
    "ridden_object": "The figure rides a giant glazed donut ring the way Kong rides the bomb.",
    "balanced_globe": "The globe is replaced by a glazed donut ring being playfully balanced.",
    "sky_object_or_helmet": "A glazed donut ring hangs in the sky like a moon, or replaces a helmet reflection.",
    "prop_or_plate": "License plate or iconic prop reads DONUT / shows the glazed ring.",
    "center_orb": "The central orb between the two figures is a glazed donut ring.",
    "gloves_colorize": "Keep the photo black-and-white except the champion's gloves, which glow in Donut brand glaze colors.",
    "plate_or_wrap": "Supercar wrap or plate carries WORLD→DONUT energy with glazed ring accents.",
    "parts_on_bench": "Every part on the assembly line is a glazed donut ring being assembled by workers.",
    "held_ticket_or_center": "Paper tickets become glazed donut rings held aloft in the pit.",
}

STYLE_PREFIX = (
    "Editorial surreal advertisement still, high craft, restrained humor. "
)

STYLE_SUFFIX = (
    "Think World.xyz meme grammar but Donut brand: one classic motif, one insert, short caption."
)


def load_catalog(name: str) -> dict:
    """Prefer JSON; fall back to YAML if PyYAML is installed."""
    json_path = CATALOG / f"{name}.json"
    yaml_path = CATALOG / f"{name}.yaml"
    if json_path.exists():
        return json.loads(json_path.read_text(encoding="utf-8"))
    if yaml_path.exists():
        try:
            import yaml  # type: ignore
        except ImportError:
            sys.exit(f"Missing {json_path.name}; or pip install PyYAML for .yaml")
        with yaml_path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    sys.exit(f"Catalog not found: {json_path} or {yaml_path}")


def sources() -> list[dict]:
    return load_catalog("sources")["sources"]


def metaphors() -> list[dict]:
    return load_catalog("metaphors")["metaphors"]


def by_id(items: list[dict], item_id: str) -> dict:
    for item in items:
        if item["id"] == item_id:
            return item
    raise SystemExit(f"Unknown id: {item_id}")


def pick_caption(meta: dict, lang: str) -> str:
    bank = meta["captions"].get(lang) or meta["captions"]["en"]
    return random.choice(bank)


def render(
    source: dict,
    meta: dict,
    *,
    lang: str = "en",
    caption: str | None = None,
    date: str = "",
    aspect: str = "1:1",
) -> str:
    caption = caption or pick_caption(meta, lang)
    slot = source.get("insert_slot", "oversized_center")
    insert_instruction = INSERT_INSTRUCTIONS.get(
        slot, "Replace the focal object with a single glazed donut ring."
    )
    tpl = TEMPLATE.read_text(encoding="utf-8")
    return (
        tpl.replace("{{source_title}}", source["title"])
        .replace("{{source_author}}", str(source.get("author", "")))
        .replace("{{source_year}}", str(source.get("year", "")))
        .replace("{{source_motif}}", source["motif"])
        .replace("{{metaphor_product}}", meta["product"])
        .replace("{{insert_slot}}", slot)
        .replace("{{caption}}", caption)
        .replace("{{date}}", date)
        .replace("{{insert_instruction}}", insert_instruction)
        .replace("{{aspect}}", aspect)
        .replace("{{style_prefix}}", STYLE_PREFIX)
        .replace("{{style_suffix}}", STYLE_SUFFIX)
    )


def cmd_list(_: argparse.Namespace) -> None:
    print("SOURCES")
    for s in sources():
        print(f"  {s['id']:28} {s['type']:14} {s['title']}")
    print("\nMETAPHORS")
    for m in metaphors():
        print(f"  {m['id']:28} {m['product'][:60]}")


def cmd_show(args: argparse.Namespace) -> None:
    s = by_id(sources(), args.id)
    print(json.dumps(s, ensure_ascii=False, indent=2))


def resolve_pair(source_id: str, metaphor_id: str | None) -> tuple[dict, dict]:
    src = by_id(sources(), source_id)
    metas = metaphors()
    if metaphor_id:
        return src, by_id(metas, metaphor_id)
    # prefer catalog suggestion
    for m in metas:
        if source_id in m.get("best_sources", []):
            return src, m
    return src, random.choice(metas)


def cmd_build(args: argparse.Namespace) -> None:
    src, meta = resolve_pair(args.source, args.metaphor)
    text = render(
        src,
        meta,
        lang=args.lang,
        caption=args.caption,
        date=args.date,
        aspect=args.aspect,
    )
    print(text)


def cmd_random(args: argparse.Namespace) -> None:
    srcs = sources()
    metas = metaphors()
    for i in range(args.count):
        src = random.choice(srcs)
        # bias to best_sources when possible
        candidates = [m for m in metas if src["id"] in m.get("best_sources", [])]
        meta = random.choice(candidates or metas)
        print("=" * 72)
        print(f"#{i + 1}  {src['id']}  ×  {meta['id']}")
        print("=" * 72)
        print(
            render(
                src,
                meta,
                lang=args.lang,
                date=args.date,
                aspect=args.aspect,
            )
        )
        print()


def cmd_export(args: argparse.Namespace) -> None:
    out = []
    for src in sources():
        for meta in metaphors():
            if args.all or src["id"] in meta.get("best_sources", []):
                out.append(
                    {
                        "source": src["id"],
                        "metaphor": meta["id"],
                        "caption_en": meta["captions"]["en"][0],
                        "caption_zh": meta["captions"]["zh"][0],
                        "prompt": render(
                            src, meta, lang="en", caption=meta["captions"]["en"][0]
                        ),
                    }
                )
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(out)} recipes → {path}")


def main() -> None:
    p = argparse.ArgumentParser(description="Donut metaphor meme prompt composer")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List sources and metaphors").set_defaults(func=cmd_list)

    sp = sub.add_parser("show", help="Show one source as JSON")
    sp.add_argument("id")
    sp.set_defaults(func=cmd_show)

    bp = sub.add_parser("build", help="Build one brief+prompt")
    bp.add_argument("source")
    bp.add_argument("--metaphor", default=None)
    bp.add_argument("--lang", choices=["en", "zh"], default="en")
    bp.add_argument("--caption", default=None)
    bp.add_argument("--date", default="")
    bp.add_argument("--aspect", default="1:1")
    bp.set_defaults(func=cmd_build)

    rp = sub.add_parser("random", help="Sample N pairings")
    rp.add_argument("--count", type=int, default=3)
    rp.add_argument("--lang", choices=["en", "zh"], default="en")
    rp.add_argument("--date", default="")
    rp.add_argument("--aspect", default="1:1")
    rp.set_defaults(func=cmd_random)

    ep = sub.add_parser("export", help="Export recipe JSON")
    ep.add_argument("out")
    ep.add_argument("--all", action="store_true", help="Full cross product (big)")
    ep.set_defaults(func=cmd_export)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
