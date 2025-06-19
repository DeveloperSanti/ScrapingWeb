def guardar_en_dataframe(productos):
    df = pd.DataFrame(productos)
    df["precio_actual"] = df["precio_actual"].str.replace(r'[^\d.]', '', regex=True)  # Eliminar símbolos
    df["precio_actual"] = pd.to_numeric(df["precio_actual"], errors="coerce")#convertimos la columna "precio_actual" a numerico
    df["precio_actual"] = np.where(df["precio_actual"] >= 50, df["precio_actual"].round(), df["precio_actual"])# Aplicar redondeo solo a los valores >= 50
 
    df["precio_anterior"] = df["precio_anterior"].str.replace(r'[^\d.]', '', regex=True)  # Eliminar símbolos
    df["precio_anterior"] = pd.to_numeric(df["precio_anterior"], errors="coerce")  # Convertir a float
    df["precio_anterior"] = df["precio_anterior"].fillna(df["precio_actual"])
    # Reemplazar NaN en "precio_anterior" con "precio_actual"
 
    df = df[df["nombre"].str.contains("iPhone", na=False)]
    df = df.sort_values(by='precio_actual', ascending=False) #Ordena los precios de mayor a menor
 
    return df
