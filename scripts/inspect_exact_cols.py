import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

# Salud
df_salud = pd.read_csv(RAW / "SALUD" / "osb_ofertasrv-ips-urgencias.csv", sep=None, engine="python", encoding="cp1252", nrows=2)
print("SALUD cols:", df_salud.columns.tolist())

# Parques
df_infra = pd.read_csv(RAW / "INFRAESTRUCTURA_ESPACIO_PUBLICO" / "5.-parques-idrd.csv", sep=";", encoding="latin1", nrows=2)
print("PARQUES cols:", df_infra.columns.tolist())

# Seguridad
df_seg = pd.read_csv(RAW / "SEGURIDAD" / "Cuadrante de Policía. Bogotá D.C.csv", sep=";", encoding="latin1", nrows=2)
print("SEGURIDAD cols:", df_seg.columns.tolist())

# Ambiente
df_amb = pd.read_csv(RAW / "AMBIENTE" / "situacion_ambiental_conflictiva.csv", sep=";", encoding="latin1", nrows=2)
print("AMBIENTE cols:", df_amb.columns.tolist())
