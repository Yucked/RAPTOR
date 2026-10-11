from pathlib import Path
import re

COLORS = {"green", "magenta", "red", "blue", "cyan", "yellow"}
WAVELENGTHS = {"405", "488", "561", "594", "647"}
REGIONS = {"inner", "outer"}
FLAGS = {"representative"}
GENOTYPES = {"wt", "appko"}
MAG_RE = re.compile(r"^\d+(?:\.\d+)?x$")
AGE_RE = re.compile(r"^\d+(?:wo|mo)$", re.I)

MARKER_ALIASES = {
    "ptau": "p-tau",
    "p-tau": "p-tau",
    "tau": "tau",
    "app": "app",
    "asyn": "asyn",
    "asynuclein": "asyn",
    "hucd": "hucd",
    "zpr3": "zpr3",
}

def parse_filename(path):
    name = Path(path).name
    stem = Path(path).stem
    tokens = stem.split("_")

    out = {
        "filename": name,
        "stem": stem,
        "age": None,
        "sample": None,
        "condition": None,
        "genotype": None,
        "region": None,
        "magnification": None,
        "replicate": None,
        "representative": False,
        "channels": [],
        "markers": [],
        "assay_marker": None,
        "unparsed": [],
    }

    consumed = set()

    for i, t in enumerate(tokens):
        tl = t.lower()

        if AGE_RE.match(tl):
            out["age"] = tl
            consumed.add(i)

        elif tl in REGIONS:
            out["region"] = tl
            consumed.add(i)

        elif tl in FLAGS:
            out["representative"] = True
            consumed.add(i)

        elif tl in GENOTYPES:
            out["genotype"] = tl
            consumed.add(i)

        elif MAG_RE.match(tl):
            out["magnification"] = tl
            consumed.add(i)

    for i, t in enumerate(tokens):
        if t in WAVELENGTHS:
            channel = {"wavelength": t, "color": None, "marker": None}
            consumed.add(i)

            if i + 1 < len(tokens) and tokens[i + 1].lower() in COLORS:
                channel["color"] = tokens[i + 1].lower()
                consumed.add(i + 1)

            if i + 2 < len(tokens):
                marker = tokens[i + 2].lower()
                if marker in MARKER_ALIASES:
                    channel["marker"] = MARKER_ALIASES[marker]
                    consumed.add(i + 2)

            out["channels"].append(channel)

    marker_set = []
    for ch in out["channels"]:
        if ch["marker"] and ch["marker"] not in marker_set:
            marker_set.append(ch["marker"])

    out["markers"] = marker_set

    structural = {"hucd", "zpr3"}
    assay_markers = [m for m in marker_set if m not in structural]
    out["assay_marker"] = assay_markers[0] if assay_markers else None

    leftovers = [
        tokens[i] for i in range(len(tokens))
        if i not in consumed
    ]

    if leftovers:
        out["sample"] = leftovers[0]

    if len(leftovers) >= 2:
        out["condition"] = leftovers[1]

    if len(leftovers) >= 3:
        out["replicate"] = leftovers[-1] if leftovers[-1].isdigit() else None

    out["unparsed"] = leftovers
    out["protein"] = out.get("assay_marker") or "unknown"
    out["subject"] = out.get("sample") or "unknown"
    out["zoom"] = out.get("magnification") or "unknown"
    out["condition"] = (
        out.get("condition")
        or out.get("genotype")
        or out.get("region")
        or "unknown"
    )
    out["replicate"] = out.get("replicate") or "1"
    out["quality_flag"] = "representative" if out.get("representative") else "ok"
    out["species_guess"] = "killifish" if out.get("age") else "human"
    
    return out