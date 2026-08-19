import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

print("--- DEMOGRAFIA ---")
f_demo = RAW / "DEMOGRAFIA" / "osb_demografia-poblacion-localidad.csv"
df_demo = pd.read_csv(f_demo, sep=";", encoding="utf-8", nrows=2)
print("Demo columns:", df_demo.columns.tolist())

print("\n--- SALUD ---")
f_salud = RAW / "SALUD" / "osb_ofertasrv-ips-urgencias.csv"
df_salud = pd.read_csv(f_salud, sep=None, engine="python", encoding="cp1252", nrows=2)
print("Salud columns:", df_salud.columns.tolist())

print("\n--- EDUCACION ---")
f_edu = RAW / "EDUCACION" / "ofertacupos_032025.geojson"
with open(f_edu, "r", encoding="utf-8") as f:
    d = json.load(f)
print("Educacion feature properties:", list(d["features"][0]["properties"].keys()))

print("\n--- MOVILIDAD ---")
f_mov = RAW / "MOVILIDAD" / "flota_vinculada_sitp_2024-12.csv"
try:
    df_mov = pd.read_csv(f_mov, sep=",", encoding="utf-8", nrows=2)
except Exception:
    df_mov = pd.read_csv(f_mov, sep=",", encoding="latin1", nrows=2)
print("Movilidad columns:", df_mov.columns.tolist())

print("\n--- INFRAESTRUCTURA ---")
f_infra = RAW / "INFRAESTRUCTURA_ESPACIO_PUBLICO" / "5.-parques-idrd.csv"
df_infra = pd.read_csv(f_infra, sep=";", encoding="latin1", nrows=2)
print("Infraestructura columns:", df_infra.columns.tolist())

print("\n--- FINANZAS ---")
f_fin = sorted(list((RAW / "FINANZAS_INVERSION_PUBLICA").glob("rivi-numero-*.txt")))[0]
df_fin = pd.read_csv(f_fin, sep=None, engine="python", encoding="latin1", nrows=2)
print("Finanzas RIVI columns:", df_fin.columns.tolist())

print("\n--- AMBIENTE ---")
f_amb = RAW / "AMBIENTE" / "situacion_ambiental_conflictiva.csv"
try:
    df_amb = pd.read_csv(f_amb, sep=";", encoding="latin1", nrows=2)
except Exception:
    df_amb = pd.read_csv(f_amb, sep=";", encoding="utf-8", nrows=2)
print("Ambiente SAC columns:", df_amb.columns.tolist())

print("\n--- SEGURIDAD ---")
f_seg = RAW / "SEGURIDAD" / "Cuadrante de Policía. Bogotá D.C.csv"
try:
    df_seg = pd.read_csv(f_seg, sep=";", encoding="latin1", nrows=2)
except Exception:
    df_seg = pd.read_csv(f_seg, sep=";", encoding="utf-8", nrows=2)
print("Seguridad columns:", df_seg.columns.tolist())
