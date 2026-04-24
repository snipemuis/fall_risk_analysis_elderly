"""Run this script to regenerate data.json for the dashboard."""
import sys
import json
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "code"))

from risico_analyse_valincidenten import RisicoAnalyseValincidenten


def safe(val):
    if val is None:
        return None
    try:
        if math.isnan(float(val)):
            return None
    except (TypeError, ValueError):
        pass
    try:
        return int(val)
    except (TypeError, ValueError):
        return val


analyse = RisicoAnalyseValincidenten()
df = analyse.data.dropna(subset=["pct_65plus"]).copy()

records = []
for _, row in df.iterrows():
    records.append({
        "gemeentecode":  safe(row["gemeentecode"]),
        "gemeentenaam":  row["gemeentenaam"],
        "inwoners":      safe(row["inwoners"]),
        "pct_65plus":    round(float(row["pct_65plus"]) * 100, 1),
        "pct_65_80":     round(float(row["pct_65_80"]) * 100, 1),
        "pct_80plus":    round(float(row["pct_80plus"]) * 100, 1),
        "n_65plus":      safe(row["n_65plus"]),
        "n_65plus_met_valrisico":                       safe(row["n_65plus_met_valrisico"]),
        "n_65plus_at_risk_met_visusproblematiek":       safe(row["n_65plus_at_risk_met_visusproblematiek"]),
        "n_vallen_65plus":                              safe(row["n_vallen_65plus"]),
        "potentieel_vallen_door_visusproblematiek_65plus": safe(row["potentieel_vallen_door_visusproblematiek_65plus"]),
        "n_65_80":       safe(row["n_65_80"]),
        "n_65_80_met_valrisico":                        safe(row["n_65_80_met_valrisico"]),
        "n_65_80_at_risk_met_visusproblematiek":        safe(row["n_65_80_at_risk_met_visusproblematiek"]),
        "n_vallen_65_80":                               safe(row["n_vallen_65_80"]),
        "potentieel_vallen_door_visusproblematiek_65_80": safe(row["potentieel_vallen_door_visusproblematiek_65_80"]),
        "n_80plus":      safe(row["n_80plus"]),
        "n_80plus_met_valrisico":                       safe(row["n_80plus_met_valrisico"]),
        "n_80plus_at_risk_met_visusproblematiek":       safe(row["n_80plus_at_risk_met_visusproblematiek"]),
        "n_vallen_80plus":                              safe(row["n_vallen_80plus"]),
        "potentieel_vallen_door_visusproblematiek_80plus": safe(row["potentieel_vallen_door_visusproblematiek_80plus"]),
        "kosten_ernstige_vallen_65plus":                    safe(row["kosten_ernstige_vallen_65plus"]),
        "kosten_ernstige_vallen_visusproblematiek_65plus":  safe(row["kosten_ernstige_vallen_visusproblematiek_65plus"]),
    })

out = Path(__file__).parent / "data.json"
out.write_text(json.dumps({"gemeenten": records}, ensure_ascii=False, indent=2))
print(f"Geschreven: {len(records)} gemeenten → {out}")
