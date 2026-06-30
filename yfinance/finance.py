import time

import yfinance as yf
import pandas as pd
import argparse

def main():
    parser = parse_arguments()
    args = parser.parse_args()

    cierres_viernes = obtener_cierres_viernes(args.tickers, args.inicio, args.fin)
    values(cierres_viernes, args.with_dates)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Descargar precios de cierre de viernes para tickers específicos.")

    parser.add_argument("--tickers", nargs='+', required=True, help="Lista de tickers separados por espacio.")
    parser.add_argument("--inicio", type=str, required=True, help="Fecha de inicio en formato YYYY-MM-DD.")
    parser.add_argument("--fin", type=str, required=True, help="Fecha de fin en formato YYYY-MM-DD.")
    parser.add_argument("--with_dates", action='store_true', help="Incluir fechas en la salida.")

    return parser

def obtener_cierres_viernes(tickers, inicio, fin)->pd.DataFrame:
    """
    Descarga datos de yfinance y devuelve solo los precios de cierre de los viernes.
    """
    resultados = pd.DataFrame()

    for ticker in tickers:
        # 1. Descargar los datos
        datos = yf.download(ticker, start=inicio, end=fin, auto_adjust=False)
        # 2. Filtrar por viernes (dayofweek 4)
        # Nota: Usamos .index porque yfinance suele poner la fecha como índice
        cierres_viernes = datos[datos.index.dayofweek == 4][['Close']]
        resultados = pd.concat([resultados, cierres_viernes.rename(columns={'Close': ticker})], axis=1)

        time.sleep(1)  # Pausa de 1 segundo entre descargas para evitar bloqueos

    return resultados

def values(data: pd.DataFrame, with_dates: bool = False):
    if(with_dates):
        print(data)
    else:
        for val in data.values.flatten().tolist():
            print(int(val))

if __name__ == "__main__":
    main()
