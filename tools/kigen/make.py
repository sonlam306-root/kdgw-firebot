import sys, os, importlib, json
sys.path.insert(0, os.path.dirname(__file__))
import kigen

mod = importlib.import_module(sys.argv[1])
stage = sys.argv[2] if len(sys.argv) > 2 else "all"
B = mod.B
d = f"/home/claude/firebot-pcb/{B['name']}"
os.makedirs(d, exist_ok=True)
pcb = f"{d}/{B['name']}.kicad_pcb"
kigen.write_schematic(B, f"{d}/{B['name']}.kicad_sch")
if stage in ("place", "all"):
    for f in os.listdir(d):
        if f.endswith((".kicad_pcb", ".kicad_pro", ".kicad_prl")):
            os.remove(f"{d}/{f}")
    kigen.build_pcb(B, pcb)
if stage in ("route", "all"):
    kigen.route(pcb, int(os.environ.get("PASSES", "40")))
    kigen.add_zones_and_fill(B, pcb)
if stage in ("place", "route", "all", "out"):
    print(json.dumps(kigen.outputs(B, d), ensure_ascii=False, indent=1))
