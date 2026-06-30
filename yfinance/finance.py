import yfinance as yf
import pandas as pd

def obtener_cierres_viernes(ticker, inicio, fin)->pd.DataFrame:
    """
    Descarga datos de yfinance y devuelve solo los precios de cierre de los viernes.
    """
    # 1. Descargar los datos
    datos = yf.download(ticker, start=inicio, end=fin, auto_adjust=False)
    # 2. Filtrar por viernes (dayofweek 4)
    # Nota: Usamos .index porque yfinance suele poner la fecha como índice
    cierres_viernes = datos[datos.index.dayofweek == 4][['Close']]
    
    return cierres_viernes

def values(data: pd.DataFrame, with_dates: bool = False):
    if(with_dates):
        print(data)
    else:
        for val in data.values.flatten().tolist():
            print(int(val))

values(obtener_cierres_viernes("CELSIA.CL", "2026-06-15", "2026-06-29"))
#values(obtener_cierres_viernes("PBRCO.CL", "2025-12-19", "2026-04-18"), True)
