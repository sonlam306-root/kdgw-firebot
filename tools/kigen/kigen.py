"""Generate a KiCad 7 project (schematic + PCB) from a Python board description,
autoroute with Freerouting, then run ERC/DRC and export fabrication files."""
import copy, json, os, re, subprocess, uuid, shutil, math
from sexp import parse, dump, Q, find, first

SYM = "/usr/share/kicad/symbols"
FPL = "/usr/share/kicad/footprints"
FR = "/home/claude/tools/fr/freerouting.jar"
_libcache = {}


def U():
    return Q(str(uuid.uuid4()))


# ------------------------------------------------------------------ symbols
def _lib(lib):
    if lib not in _libcache:
        root = parse(open(f"{SYM}/{lib}.kicad_sym").read())
        _libcache[lib] = {e[1]: e for e in find(root, "symbol")}
    return _libcache[lib]


def lib_symbol(lib_id):
    lib, name = lib_id.split(":")
    syms = _lib(lib)
    s = copy.deepcopy(syms[name])
    ext = first(s, "extends")
    if ext:
        parent = lib_symbol(f"{lib}:{ext[1]}")[1]
        pname = parent[1]
        base = copy.deepcopy(parent)
        base[1] = Q(name)
        childprops = {p[1]: p for p in find(s, "property")}
        newb = []
        for e in base:
            if isinstance(e, list) and e and e[0] == "property" and e[1] in childprops:
                newb.append(childprops.pop(e[1]))
            elif isinstance(e, list) and e and e[0] == "symbol":
                e[1] = Q(e[1].replace(pname + "_", name + "_", 1))
                newb.append(e)
            else:
                newb.append(e)
        for p in childprops.values():
            newb.insert(3, p)
        s = newb
    full = copy.deepcopy(s)
    full[1] = Q(lib_id)
    return full, s


def sym_pins(symnode):
    """pins of unit 1 / body style 1: number -> (x, y, angle, type, name)"""
    name = symnode[1].split(":")[-1]
    pins = {}
    for sub in find(symnode, "symbol"):
        m = re.match(r".*_(\d+)_(\d+)$", sub[1])
        if not m or m.group(1) not in ("0", "1") or m.group(2) not in ("0", "1"):
            continue
        for p in find(sub, "pin"):
            at = first(p, "at")
            num = first(p, "number")[1]
            pins[num] = (float(at[1]), float(at[2]), int(float(at[3])) if len(at) > 3 else 0, p[1], first(p, "name")[1])
    return pins


def sym_bbox(symnode):
    xs, ys = [], []
    for x, y, *_ in sym_pins(symnode).values():
        xs.append(x); ys.append(y)
    for sub in find(symnode, "symbol"):
        for r in find(sub, "rectangle"):
            for k in ("start", "end"):
                v = first(r, k); xs.append(float(v[1])); ys.append(float(v[2]))
    if not xs:
        xs, ys = [0], [0]
    return min(xs), min(ys), max(xs), max(ys)


def prop(name, val, x, y, hide=False, ang=0):
    eff = ["effects", ["font", ["size", 1.27, 1.27]]]
    if hide:
        eff.append("hide")
    return ["property", Q(name), Q(val), ["at", x, y, ang], eff]


def snap(v, g=2.54):
    return round(v / g) * g


# ------------------------------------------------------------------ schematic
def write_schematic(B, path):
    root_uuid = Q(str(uuid.uuid5(uuid.NAMESPACE_URL, "firebot/" + B["name"])))
    libsyms, items = {}, []
    blocks = []
    for p in B["parts"]:
        if p.get("blk") not in blocks:
            blocks.append(p.get("blk"))
    W, H = 420.0, 297.0
    cols = [[15.24, 25.4], [W / 2 + 5.08, 25.4]]
    colw = W / 2 - 22
    for blk in blocks:
        ci = 0 if cols[0][1] <= cols[1][1] else 1
        x0, y = cols[ci]
        items.append(["text", Q(blk), ["at", x0, y, 0], ["effects", ["font", ["size", 2.5, 2.5], "bold"], ["justify", "left", "bottom"]], ["uuid", U()]])
        y += 5.08
        x = x0
        rowh = 0
        for p in [q for q in B["parts"] if q.get("blk") == blk]:
            full, raw = lib_symbol(p["sym"])
            libsyms[p["sym"]] = full
            pins = sym_pins(full)
            minx, miny, maxx, maxy = sym_bbox(full)
            lab = max([len(n) for n in p["pins"].values()] + [3]) * 1.3 + 4
            left = (-minx + (lab if any(a == 0 for (_, _, a, _, _) in pins.values()) else 6))
            right = (maxx + (lab if any(a == 180 for (_, _, a, _, _) in pins.values()) else 6))
            right = max(right, len(p["val"]) * 1.27 * 0.55 - left + 4)
            top = maxy + 5 + (6 if any(a == 270 for (_, _, a, _, _) in pins.values()) else 0)
            bot = -miny + 6 + (6 if any(a == 90 for (_, _, a, _, _) in pins.values()) else 0)
            if x + left + right > x0 + colw:
                x = x0
                y += rowh + 3
                rowh = 0
            sx, sy = snap(x + left), snap(y + top)
            p["_sch"] = (sx, sy)
            p["_uuid"] = Q(str(uuid.uuid5(uuid.NAMESPACE_URL, "firebot/" + B["name"] + "/" + p["ref"])))
            node = ["symbol", ["lib_id", Q(p["sym"])], ["at", sx, sy, 0], ["unit", 1],
                    ["in_bom", "yes" if not p.get("nobom") else "no"], ["on_board", "yes" if p.get("fp") else "no"], ["dnp", "no"], ["uuid", p["_uuid"]],
                    prop("Reference", p["ref"], sx, sy - maxy - 2.54),
                    prop("Value", p["val"], sx, sy - miny + 2.54),
                    prop("Footprint", p.get("fp", ""), sx, sy, True),
                    prop("Datasheet", "", sx, sy, True)]
            if p.get("note"):
                node.append(prop("Ghi chú", p["note"], sx, sy - miny + 5.08, True))
            for num in pins:
                node.append(["pin", Q(num), ["uuid", U()]])
            node.append(["instances", ["project", Q(B["name"]), ["path", Q("/" + root_uuid), ["reference", Q(p["ref"])], ["unit", 1]]]])
            items.append(node)
            for num, (px, py, a, ptype, pname) in pins.items():
                cx, cy = sx + px, sy - py
                net = p["pins"].get(num)
                if net is None:
                    if ptype != "no_connect" and not (ptype == "passive" and pname == "GND" and False):
                        items.append(["no_connect", ["at", cx, cy], ["uuid", U()]])
                    continue
                la = {0: 180, 180: 0, 90: 270, 270: 90}[a % 360]
                just = {0: ["justify", "left", "bottom"], 180: ["justify", "right", "bottom"],
                        90: ["justify", "left", "bottom"], 270: ["justify", "right", "bottom"]}[la]
                items.append(["label", Q(net), ["at", cx, cy, la], ["fields_autoplaced"],
                              ["effects", ["font", ["size", 1.27, 1.27]], just], ["uuid", U()]])
            x += left + right + 2.54
            rowh = max(rowh, top + bot)
        y += rowh + 8
        cols[ci] = [x0, y]
    y = max(c[1] for c in cols)
    if y > H - 20:
        W, H, paper = 594.0, 420.0, "A2"
    else:
        paper = "A3"
    sch = ["kicad_sch", ["version", 20230121], ["generator", "eeschema"], ["uuid", root_uuid], ["paper", Q(paper)],
           ["title_block", ["title", Q(B["title"])], ["date", Q(B["date"])], ["rev", Q(B["rev"])], ["company", Q("Arden")],
            ["comment", 1, Q(B.get("comment", ""))]],
           ["lib_symbols"] + list(libsyms.values())] + items + [
           ["sheet_instances", ["path", Q("/"), ["page", Q("1")]]]]
    open(path, "w").write(dump(sch) + "\n")
    return y


# ------------------------------------------------------------------ PCB
def build_pcb(B, path):
    import pcbnew
    mm = pcbnew.FromMM
    V = lambda x, y: pcbnew.VECTOR2I(mm(B["ox"] + x), mm(B["oy"] + y))
    board = pcbnew.NewBoard(path)
    ds = board.GetDesignSettings()
    ds.SetCopperLayerCount(2)
    ds.m_TrackMinWidth = mm(0.2); ds.m_MinClearance = mm(0.2); ds.m_ViasMinSize = mm(0.6)
    ds.m_ViasMinAnnularWidth = mm(0.13); ds.m_MinThroughDrill = mm(0.3); ds.m_CopperEdgeClearance = mm(0.4)
    nets = {}
    allnets = sorted({n for p in B["parts"] for n in p["pins"].values()})
    for n in allnets:
        ni = pcbnew.NETINFO_ITEM(board, n)
        board.Add(ni)
        nets[n] = ni
    for p in B["parts"]:
        if not p.get("fp"):
            continue
        lib, name = p["fp"].split(":")
        fp = pcbnew.FootprintLoad(f"{FPL}/{lib}.pretty", name)
        if fp is None:
            raise RuntimeError("missing footprint " + p["fp"])
        fp.SetFPID(pcbnew.LIB_ID(lib, name))
        fp.SetReference(p["ref"]); fp.SetValue(p["val"])
        if "_uuid" in p:
            fp.SetPath(pcbnew.KIID_PATH("/" + p["_uuid"]))
        x, y, r = p["at"]
        board.Add(fp)
        if p.get("side") == "B":
            fp.Flip(fp.GetPosition(), False)
        fp.SetPosition(V(x, y)); fp.SetOrientationDegrees(r)
        fp.Value().SetVisible(False)
        rt = fp.Reference()
        rt.SetTextSize(pcbnew.VECTOR2I(mm(0.9), mm(0.9))); rt.SetTextThickness(mm(0.15))
        if p.get("hideref"):
            rt.SetVisible(False)
        for pad in fp.Pads():
            n = p["pins"].get(pad.GetNumber())
            if n:
                pad.SetNet(nets[n])
    # outline
    w, h, rc = B["w"], B["h"], B.get("corner", 2.0)
    def seg(a, b):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(V(*a)); s.SetEnd(V(*b)); s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); board.Add(s)
    def arc(c, st, ang):
        s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_ARC)
        s.SetCenter(V(*c)); s.SetStart(V(*st)); s.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(ang, pcbnew.DEGREES_T))
        s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(mm(0.1)); board.Add(s)
    seg((rc, 0), (w - rc, 0)); seg((w, rc), (w, h - rc)); seg((w - rc, h), (rc, h)); seg((0, h - rc), (0, rc))
    arc((w - rc, rc), (w - rc, 0), 90); arc((w - rc, h - rc), (w, h - rc), 90)
    arc((rc, h - rc), (rc, h), 90); arc((rc, rc), (0, rc), 90)
    # mounting holes
    for i, (hx, hy) in enumerate(B["holes"]):
        fp = pcbnew.FootprintLoad(f"{FPL}/MountingHole.pretty", B["hole_fp"])
        fp.SetReference(f"H{i+1}"); fp.Reference().SetVisible(False); fp.Value().SetVisible(False)
        board.Add(fp); fp.SetPosition(V(hx, hy))
    # texts
    for t in B.get("texts", []):
        txt, x, y = t[0], t[1], t[2]
        rot = t[3] if len(t) > 3 else 0
        layer = (t[4] if len(t) > 4 else "F.SilkS").replace("SilkS", "Silkscreen")
        size = t[5] if len(t) > 5 else 1.0
        pt = pcbnew.PCB_TEXT(board); pt.SetText(txt); pt.SetPosition(V(x, y))
        pt.SetLayer(board.GetLayerID(layer)); pt.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
        pt.SetTextThickness(mm(max(0.15, size * 0.15))); pt.SetTextAngleDegrees(rot)
        if layer.startswith("B."):
            pt.SetMirrored(True)
        board.Add(pt)
    pcbnew.SaveBoard(path, board)
    # net classes into project file
    pro = path.replace(".kicad_pcb", ".kicad_pro")
    pj = json.load(open(pro)) if os.path.exists(pro) else {}
    classes = [{"name": "Default", "track_width": 0.3, "clearance": 0.2, "via_diameter": 0.7, "via_drill": 0.35,
                "diff_pair_gap": 0.25, "diff_pair_width": 0.2, "diff_pair_via_gap": 0.25, "microvia_diameter": 0.3,
                "microvia_drill": 0.1, "line_style": 0, "pcb_color": "rgba(0, 0, 0, 0.000)",
                "schematic_color": "rgba(0, 0, 0, 0.000)", "wire_width": 6, "bus_width": 12}]
    pats = []
    for cname, (tw, cl, vd, vdr), members in B["netclasses"]:
        c = dict(classes[0]); c.update(name=cname, track_width=tw, clearance=cl, via_diameter=vd, via_drill=vdr)
        classes.append(c)
        pats += [{"netclass": cname, "pattern": m} for m in members]
    pj.setdefault("net_settings", {})
    pj["net_settings"].update({"classes": classes, "meta": {"version": 3}, "netclass_patterns": pats,
                               "netclass_assignments": None})
    pj.setdefault("meta", {"filename": os.path.basename(pro), "version": 1})
    json.dump(pj, open(pro, "w"), indent=2)


def route(path, passes=40):
    import pcbnew
    board = pcbnew.LoadBoard(path)
    dsn = path.replace(".kicad_pcb", ".dsn"); ses = path.replace(".kicad_pcb", ".ses")
    pcbnew.ExportSpecctraDSN(board, dsn)
    if os.path.exists(ses):
        os.remove(ses)
    r = subprocess.run(["xvfb-run", "-a", "java", "-jar", FR, "-de", dsn, "-do", ses, "-mp", str(passes), "-mt", "1"],
                       capture_output=True, text=True, timeout=1500)
    if not os.path.exists(ses):
        print(r.stdout[-3000:], r.stderr[-3000:])
        raise RuntimeError("freerouting failed")
    import_ses(board, ses)
    pcbnew.SaveBoard(path, board)


def import_ses(board, ses):
    import pcbnew
    t = parse(open(ses).read())
    routes = first(t, "routes")
    res = first(routes, "resolution")
    scale = {"um": 1e-3, "mm": 1.0, "mil": 0.0254}[res[1]] / float(res[2])
    P = lambda x, y: pcbnew.VECTOR2I(pcbnew.FromMM(float(x) * scale), pcbnew.FromMM(-float(y) * scale))
    lay = {"F.Cu": pcbnew.F_Cu, "B.Cu": pcbnew.B_Cu}
    for tr in list(board.GetTracks()):
        board.Remove(tr)
    nout = first(routes, "network_out")
    n_w = n_v = 0
    for net in find(nout, "net"):
        ni = board.FindNet(net[1])
        for w in find(net, "wire"):
            pth = first(w, "path")
            layer, width = pth[1], float(pth[2]) * scale
            pts = pth[3:]
            for i in range(0, len(pts) - 2, 2):
                trk = pcbnew.PCB_TRACK(board)
                trk.SetStart(P(pts[i], pts[i + 1])); trk.SetEnd(P(pts[i + 2], pts[i + 3]))
                trk.SetWidth(pcbnew.FromMM(width)); trk.SetLayer(lay[layer]); trk.SetNet(ni)
                board.Add(trk); n_w += 1
        for v in find(net, "via"):
            m = re.search(r"_(\d+):(\d+)_um", v[1])
            dia, drl = (int(m.group(1)) / 1000, int(m.group(2)) / 1000) if m else (0.7, 0.35)
            via = pcbnew.PCB_VIA(board)
            via.SetPosition(P(v[2], v[3])); via.SetWidth(pcbnew.FromMM(dia)); via.SetDrill(pcbnew.FromMM(drl))
            via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); via.SetNet(ni)
            board.Add(via); n_v += 1
    print("imported", n_w, "segments", n_v, "vias")


def add_zones_and_fill(B, path):
    import pcbnew
    mm = pcbnew.FromMM
    board = pcbnew.LoadBoard(path)
    for zname, layer in B.get("zones", [("GND", "F.Cu"), ("GND", "B.Cu")]):
        net = board.FindNet(zname)
        z = pcbnew.ZONE(board)
        z.SetLayer(board.GetLayerID(layer)); z.SetNet(net)
        z.SetLocalClearance(mm(0.35)); z.SetMinThickness(mm(0.25))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
        z.SetThermalReliefGap(mm(0.4)); z.SetThermalReliefSpokeWidth(mm(0.5))
        ol = z.Outline(); ol.NewOutline()
        e = 0.3
        for x, y in [(e, e), (B["w"] - e, e), (B["w"] - e, B["h"] - e), (e, B["h"] - e)]:
            ol.Append(mm(B["ox"] + x), mm(B["oy"] + y))
        board.Add(z)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    # GND stitching vias wherever there is room (ties islands of the two GND pours together)
    gnd = board.FindNet("GND")
    keep = 1.2
    items = [t for t in board.GetTracks()] + [p for p in board.GetPads()]
    holes = [(B["ox"] + hx, B["oy"] + hy) for hx, hy in B["holes"]]
    added = 0
    step = 4.0
    y = 3.0
    while y < B["h"] - 2.5:
        x = 3.0
        while x < B["w"] - 2.5:
            ax, ay = B["ox"] + x, B["oy"] + y
            pos = pcbnew.VECTOR2I(mm(ax), mm(ay))
            ok = all(math.hypot(ax - hx, ay - hy) > 4.5 for hx, hy in holes)
            if ok:
                for it in items:
                    if it.HitTest(pos, mm(keep)):
                        ok = False; break
            if ok:
                fz = [z for z in board.Zones() if z.GetNetname() == "GND"]
                ok = any(z.GetFilledPolysList(z.GetLayer()).Contains(pos) for z in fz)
            if ok:
                v = pcbnew.PCB_VIA(board); v.SetPosition(pos); v.SetWidth(mm(0.7)); v.SetDrill(mm(0.35))
                v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNet(gnd); board.Add(v); items.append(v); added += 1
            x += step
        y += step
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    print("stitch vias", added)
    pcbnew.SaveBoard(path, board)


def outputs(B, d):
    name = B["name"]
    pcb = f"{d}/{name}.kicad_pcb"; sch = f"{d}/{name}.kicad_sch"
    res = {}
    r = subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "drc.py"), pcb, f"{d}/drc.rpt"], capture_output=True, text=True)
    res["drc"] = r.stdout.strip().splitlines()[-1:] if r.stdout.strip() else r.stderr[-500:]
    cnt = {}
    for p in B["parts"]:
        for n in p["pins"].values():
            cnt[n] = cnt.get(n, 0) + 1
    res["single_pin_nets"] = [n for n, c in cnt.items() if c < 2]
    g = f"{d}/gerber"; shutil.rmtree(g, ignore_errors=True); os.makedirs(g)
    subprocess.run(["kicad-cli", "pcb", "export", "gerbers", "--layers", "F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts",
                    "--subtract-soldermask", "--no-x2", "-o", g + "/", pcb], capture_output=True)
    subprocess.run(["kicad-cli", "pcb", "export", "drill", "--format", "excellon", "--excellon-separate-th", "--generate-map", "--map-format", "pdf", "-o", g + "/", pcb], capture_output=True)
    shutil.make_archive(f"{d}/{name}_gerber", "zip", g)
    subprocess.run(["kicad-cli", "sch", "export", "pdf", "-o", f"{d}/{name}_schematic.pdf", sch], capture_output=True)
    groups = {}
    for p in B["parts"]:
        if p.get("nobom") or not p.get("fp"):
            continue
        groups.setdefault((p["val"], p["fp"]), []).append(p["ref"])
    import csv
    with open(f"{d}/{name}_bom.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh); w.writerow(["Ref", "Giá trị", "Footprint", "SL"])
        key = lambda r: (re.sub(r"\d", "", r), int(re.sub(r"\D", "", r) or 0))
        for (val, fp), refs in sorted(groups.items(), key=lambda kv: key(sorted(kv[1], key=key)[0])):
            refs = sorted(refs, key=key)
            w.writerow([" ".join(refs), val, fp.split(":")[1], len(refs)])
    subprocess.run(["kicad-cli", "pcb", "export", "pos", "--format", "csv", "--units", "mm", "-o", f"{d}/{name}_cpl.csv", pcb], capture_output=True)
    for tag, layers, extra in [("top", "F.Cu,F.SilkS,Edge.Cuts", []), ("bottom", "B.Cu,B.SilkS,Edge.Cuts", ["--mirror"])]:
        svg = f"{d}/{name}_{tag}.svg"
        subprocess.run(["kicad-cli", "pcb", "export", "svg", "--layers", layers, "--exclude-drawing-sheet", "--page-size-mode", "2"] + extra + ["-o", svg, pcb], capture_output=True)
        subprocess.run(["rsvg-convert", "-z", "6", "-b", "white", "-o", svg.replace(".svg", ".png"), svg], capture_output=True)
    return res
