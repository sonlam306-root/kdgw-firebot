import sys, re, pcbnew
b = pcbnew.LoadBoard(sys.argv[1])
pcbnew.WriteDRCReport(b, sys.argv[2], pcbnew.EDA_UNITS_MILLIMETRES, True)
t = open(sys.argv[2]).read()
items = re.findall(r"^\[(\w+)\]:.*?\n\s+.*?Severity: (\w+)", t, re.M)
err = {}
for k, s in items:
    if s == "error":
        err[k] = err.get(k, 0) + 1
u = re.search(r"Found (\d+) unconnected pads", t)
print("DRC errors:", sum(err.values()), err, "| unconnected:", u.group(1) if u else "?")
