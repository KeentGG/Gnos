#!/usr/bin/env python3
"""Build an offline JSXGraph artifact from a starter or an authored JavaScript scene."""
import argparse
from pathlib import Path
import re

SKILL = Path(__file__).resolve().parents[1]
SIMULATION = SKILL.parent / "lesson-design/templates/simulation.html"
PALETTES = ("luxe", "wine", "forest", "blue")
EXAMPLES = ("derivative", "gradient-descent", "supply-demand")


def fragment(source, tag, identifier):
    match = re.search(rf'<{tag}\b[^>]*\bid="{identifier}"[^>]*>(.*?)</{tag}>', source, re.S)
    if not match:
        raise ValueError(f"Simulation template is missing {identifier}")
    return match.group(1)


def inline_script(source):
    # HTML parses a closing script tag even inside a JavaScript string.
    return re.sub(r"</script", r"<\\/script", source, flags=re.I)


def build_graph(scene, palette="luxe"):
    if palette not in PALETTES:
        raise ValueError(f"Unknown palette: {palette}")
    simulation = SIMULATION.read_text()
    vendor = SKILL / "assets/vendor"
    license_text = (vendor / "LICENSE.MIT").read_text()
    third_party = (vendor / "jsxgraphcore.js.LICENSE.txt").read_text()
    values = {
        "PALETTE": palette,
        "SIMULATION_STYLE": fragment(simulation, "style", "simulation-style"),
        "SHELL_SCRIPT": inline_script(fragment(simulation, "script", "simulation-shell-script")),
        "JSXGRAPH_RUNTIME": inline_script("/* JSXGraph 1.13.3\n" + license_text + "\n" + third_party.replace("*/", "* /") + "\n*/\n" + (vendor / "jsxgraphcore.js").read_text()),
        "GRAPH_SCRIPT": inline_script((SKILL / "templates/graph.js").read_text()),
        "SCENE_SCRIPT": inline_script(Path(scene).read_text()),
    }
    template = (SKILL / "templates/graph.html").read_text()
    # Substitute only original template tokens, never code that was inserted.
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda match: values[match.group(1)], template)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--example", choices=EXAMPLES)
    source.add_argument("--scene", type=Path)
    parser.add_argument("--palette", choices=PALETTES, default="luxe")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        scene = args.scene or SKILL / f"examples/{args.example}.js"
        content = build_graph(scene, args.palette)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Graph build failed: {exc}\n")
    print(args.output)


if __name__ == "__main__":
    main()
