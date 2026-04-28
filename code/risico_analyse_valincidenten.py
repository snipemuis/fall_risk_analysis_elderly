import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

import constants as c
from load_cbs_data import load_cbs_bevolking, load_cbs_ouderen, population_NL, percentage_ouderen_NL

_LEEFTIJDSGROEPEN = {
    "65plus": "pct_65plus",
    "65_80":  "pct_65_80",
    "80plus": "pct_80plus",
}


def geschatte_kosten_vallen(
    df: pd.DataFrame, prefix: str, risico_ernstig_valincident: float
) -> pd.DataFrame:
    """
    Voegt kostkolommen toe per leeftijdsgroep.

    Kalibratie: risico_ernstig_valincident = 105.000 / (pop_NL × %ouderen × valrisico_incidentie)
    zodat sum(kosten_alle) ≈ € 1,1 mrd (VeiligheidNL 2020).

    1. kosten_ernstige_vallen_{prefix}
       = n_{prefix}_met_valrisico × risico_ernstig_valincident × direct_cost_pp

    2. kosten_ernstige_vallen_visusproblematiek_{prefix}
       = (potentieel_vallen_visus / gemiddeld_aantal_vallen) × risico_ernstig_valincident × direct_cost_pp
       → aandeel van kosten toe te schrijven aan visusproblematiek
    """
    n_val       = f"n_{prefix}_met_valrisico"
    potentieel  = f"potentieel_vallen_door_visusproblematiek_{prefix}"
    kosten_alle = f"kosten_ernstige_vallen_{prefix}"
    kosten_vis  = f"kosten_ernstige_vallen_visusproblematiek_{prefix}"

    df[kosten_alle] = (
        df[n_val] * risico_ernstig_valincident * c.direct_cost_pp
    ).round().astype("Int64")

    df[kosten_vis] = (
        df[potentieel] / c.gemiddeld_aantal_vallen * risico_ernstig_valincident * c.direct_cost_pp
    ).round().astype("Int64")

    return df


class LeeftijdsgroepAnalyse:
    """Gefilterde view van de risico-analyse voor één leeftijdsgroep."""

    def __init__(self, df: pd.DataFrame, prefix: str):
        self.prefix = prefix
        cols = ["gemeentecode", "gemeentenaam", "inwoners"] + [
            col for col in df.columns if col.endswith(f"_{prefix}")
        ]
        self.data = df[cols].copy()

    def __repr__(self) -> str:
        return f"LeeftijdsgroepAnalyse(prefix='{self.prefix}', {len(self.data)} gemeenten)"


class RisicoAnalyseValincidenten:
    """Berekent valrisico-indicatoren per gemeente op basis van CBS-data."""

    percentage_sterfgevallen: float = (17 * 365) / c.ernstige_valincidenten

    def __init__(self):
        self._df_base = self._load_en_merge()
        self.risico_ernstig_valincident = self._bereken_risico_ernstig_valincident()
        self.data = self._bereken_risicos(self._df_base)
        self.plus65 = LeeftijdsgroepAnalyse(self.data, "65plus")
        self.j65_80 = LeeftijdsgroepAnalyse(self.data, "65_80")
        self.plus80 = LeeftijdsgroepAnalyse(self.data, "80plus")
        self.totaal_nederland = self._bereken_totaal_nl()

    def _load_en_merge(self) -> pd.DataFrame:
        bevolking = load_cbs_bevolking()
        ouderen = load_cbs_ouderen()

        df = bevolking.merge(
            ouderen,
            left_on="gemeentenaam",
            right_on="gemeente",
            how="left",
        ).drop(columns=["gemeente"])

        for col in ["pct_65plus", "pct_65_80", "pct_80plus"]:
            df[col] = df[col] / 100

        n_missing = df["pct_65plus"].isna().sum()
        if n_missing:
            print(f"Waarschuwing: {n_missing} gemeenten zonder ouderendata na merge.")

        return df

    def _bereken_risico_ernstig_valincident(self) -> float:
        pct_ouderen_nl = percentage_ouderen_NL() / 100
        pop_nl = population_NL()
        return c.ernstige_valincidenten / (pop_nl * pct_ouderen_nl * c.valrisico_incidentie)

    def _bereken_voor_groep(self, df: pd.DataFrame, prefix: str, pct_col: str) -> pd.DataFrame:
        n          = f"n_{prefix}"
        n_val      = f"n_{prefix}_met_valrisico"
        n_vis      = f"n_{prefix}_at_risk_met_visusproblematiek"
        n_vallen   = f"n_vallen_{prefix}"
        potentieel = f"potentieel_vallen_door_visusproblematiek_{prefix}"
        sterfgeval = f"sterfgevallen_door_visusproblematiek_{prefix}"

        df[n]          = (df["inwoners"] * df[pct_col]).round().astype("Int64")
        df[n_val]      = (df[n] * c.valrisico_incidentie).round().astype("Int64")
        df[n_vis]      = (df[n_val] * c.percentage_onbekende_visusproblematiek).round().astype("Int64")
        df[n_vallen]   = (df[n_vis] * c.gemiddeld_aantal_vallen).round().astype("Int64")
        df[potentieel] = (df[n_vallen] - df[n_vallen] / 1.35).round().astype("Int64")
        df[sterfgeval] = (
            df[potentieel] * self.risico_ernstig_valincident * self.percentage_sterfgevallen
        ).round().astype("Int64")

        return df

    def _bereken_risicos(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for prefix, pct_col in _LEEFTIJDSGROEPEN.items():
            df = self._bereken_voor_groep(df, prefix, pct_col)
            df = geschatte_kosten_vallen(df, prefix, self.risico_ernstig_valincident)
        return df

    def _bereken_totaal_nl(self) -> dict:
        df = self.data.dropna(subset=["pct_65plus"])
        exclude = {"gemeentecode", "gemeentenaam", "pct_65plus", "pct_65_80", "pct_80plus"}
        num_cols = [col for col in df.columns if col not in exclude]

        totaal = {col: int(df[col].sum()) for col in num_cols}
        totaal["gemeentecode"] = None
        totaal["gemeentenaam"] = "Nederland (alle gemeenten)"
        totaal["pct_65plus"] = totaal["n_65plus"] / totaal["inwoners"]
        totaal["pct_65_80"]  = totaal["n_65_80"]  / totaal["inwoners"]
        totaal["pct_80plus"] = totaal["n_80plus"]  / totaal["inwoners"]
        return totaal

    def __repr__(self) -> str:
        return (
            f"RisicoAnalyseValincidenten("
            f"risico_ernstig_valincident={self.risico_ernstig_valincident:.4f}, "
            f"percentage_sterfgevallen={self.percentage_sterfgevallen:.4f})"
        )


if __name__ == "__main__":
    analyse = RisicoAnalyseValincidenten()
    print(analyse)
    print()
    print(analyse.plus65.data.head(5).to_string())
