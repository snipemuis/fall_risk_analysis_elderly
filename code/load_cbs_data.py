import io
from pathlib import Path
import requests
import pandas as pd

URL = "https://www.cbs.nl/-/media/_excel/2025/44/voorlopige-bevolkings-gegevens-20251001.xlsx"

def load_cbs_bevolking() -> pd.DataFrame:
    response = requests.get(URL)
    response.raise_for_status()

    df = pd.read_excel(
        io.BytesIO(response.content),
        sheet_name="Tabel 1",
        header=10,
        usecols=[0, 1, 3],
    )
    df.columns = ["gemeentecode", "gemeentenaam", "inwoners"]
    df = df.dropna(subset=["gemeentecode", "inwoners"])
    df["gemeentecode"] = df["gemeentecode"].astype(int)
    df["inwoners"] = df["inwoners"].astype(int)
    return df.reset_index(drop=True)

def population_NL() -> int:
    df = load_cbs_bevolking()
    return df["inwoners"].sum()

def percentage_ouderen_NL() -> float:
    df_bevolking = load_cbs_bevolking()
    df_ouderen = load_cbs_ouderen()
    
    total_population = df_bevolking["inwoners"].sum()
    total_ouderen = (df_ouderen["pct_65plus"] / 100 * df_bevolking["inwoners"]).sum()
    
    return (total_ouderen / total_population) * 100

OUDEREN_CSV = (
    Path(__file__).parent.parent
    / "data"
    / "Ouderen per gemeente, 2025 (%).csv"
)

_GEMEENTE_NAAM_FIXES = {
    "Groningen (gemeente)":           "Groningen",
    "Utrecht (gemeente)":             "Utrecht",
    "'s-Gravenhage (gemeente)":       "'s-Gravenhage",
    "Bergen (L.)":                    "Bergen (L)",
    "Bergen (NH.)":                   "Bergen (N-H)",
    "Hengelo (O.)":                   "Hengelo (O)",
    "Laren (NH.)":                    "Laren",
    "Rijswijk (ZH.)":                 "Rijswijk",
    "Middelburg (Z.)":                "Middelburg",
    "Beek (L.)":                      "Beek",
    "Stein (L.)":                     "Stein",
    "Nuenen, Gerwen en Nederwetten":  "Nuenen c.a.",
    "Súdwest-Fryslân":                "Súdwest Fryslân",
}


def load_cbs_ouderen() -> pd.DataFrame:
    df = pd.read_csv(OUDEREN_CSV, sep=";", encoding="utf-8-sig", decimal=",")
    df.columns = ["gemeente", "pct_65plus", "pct_65_80", "pct_80plus"]
    df["gemeente"] = df["gemeente"].replace(_GEMEENTE_NAAM_FIXES)
    return df.reset_index(drop=True)

if __name__ == "__main__":
    df = load_cbs_bevolking()
    print(df.head(10).to_string())
    print(f"\n{len(df)} gemeenten, totaal: {df['inwoners'].sum():,}")
