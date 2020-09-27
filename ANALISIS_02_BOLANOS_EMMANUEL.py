# Importamos las librerías a usar
import pandas as pd
import numpy as np

# Abrimos el archivo, leemos los valores y creamos una
# dataframe con ellos en la variable df
with open("synergy_logistics_database.csv", "r") as database:
    df = pd.read_csv(database, index_col=0)

# OP.1 RUTAS IN/OUT. Deberíamos enfocarnos en las 10 rutas mas demandadas.
# Obtenemos los nombres de las columnas
# y los asignamos a una variable
cols = df.columns
#print(cols)

# Tomamos las columnas que nos interesan para realizar
# el análisis propuesto en la opción 1
util_cols_1 = [cols[0], cols[1], cols[2]]

# Filtramos la df para solo mostrar las columnas
# que nos interesan
df_op1 = df.loc[:, util_cols_1]

# Agrupamos con groupby las filas donde la columna de dirección,
# origen y destino coinciden. Además, usando la función de agregado
# size() calculamos el tamaño de cada grupo (que sería la cantidad
# de veces que cada ruta es usada) y lo agregamos como una serie.
# Reiniciamos el índice para mostrar cada fila por separado y asignamos
# el nombre 'count' a la columna creada por size()
df_op1 = df_op1.groupby(util_cols_1).size().reset_index(name='count')

# Ordenamos los valores en orden descendente. El argumento inplace
# indica que el cambio toma lugar en la misma variable
df_op1.sort_values('count', ascending=False, inplace=True)

# Usamos slicing para seleccionar solo las primeras 10 rutas
df_ans1 = df_op1[:10]

# Mostramos el resultado
# print(df_ans1)

# OP.2 MEDIO DE TRANSPORTE. Los 3 medios mas importantes según el valor
# de las in/out. Cual se puede reducir.

# Tomamos las columnas que nos interesan para realizar
# el análisis propuesto en la opción 2
util_cols_2 = [cols[6], cols[8]]

# Filtramos la df para solo mostrar las columnas
# que nos interesan
df_op2 = df.loc[:, util_cols_2]

# Una vez más agrupamos nuestra dataframe, en esta ocasión lo hacemos
# respecto a la columna de modo de transporte y obtenemos la suma, el
# conteo de viajes y el promedio de ganancias para cada grupo.
# Reiniciamos para volver al formato de nuestra dataframe
df_op2 = df_op2.groupby('transport_mode').total_value.\
    agg(['sum', 'count', 'mean']).reset_index()

# Imprimimos el resultado y nos damos cuenta de que los números son
# grandes, lo cual dificulta apreciar la diferencia entre estos.
# Los convertimos a porcentajes para facilitar su comparación.
# print(df_op2)

# Tomamos la porción de nuestra dataframe que contiene los valores
# máximos para cada columna
max_by_column = df_op2.iloc[0:4, 1:4].max()

# Dividimos cada columna por su máximo y renombramos las columnas
max_rets = df_op2.iloc[0:4, 1:4]/max_by_column
max_rets = max_rets.rename(columns={'sum': 'norm_sum',
                                    'count': 'norm_count', 'mean': 'norm_mean'})

# Agregamos los valores obtenidos a nuestra dataframe anterior e imprimimos
df_op2 = df_op2.join(max_rets)
# print(df_op2)

# OP.3 VALOR TOTAL DE IN/OUT. Si nos enfocamos en los países que generan
# el 80% del valor de los in/outs, que países serian esos.

total_values = df.groupby('direction').total_value.sum().reset_index(name='totals')

countries_value = df.groupby(['direction', 'origin']).total_value.sum().reset_index()
# print(countries_value)

cond = countries_value['direction'] == 'Exports'

countries_value['total_value'] = countries_value['total_value'].\
    mask(cond, countries_value['total_value'].div(total_values.iloc[0, 1]))
countries_value['total_value'] = countries_value['total_value'].\
    mask(~cond, countries_value['total_value'].div(total_values.iloc[1, 1]))

countries_value.sort_values(['direction', 'total_value'],
                            ascending=[True, False], inplace=True)

countries_value['cum_val'] = countries_value['total_value'].\
    mask(cond, countries_value['total_value'].cumsum())
countries_value['cum_val'] = countries_value['cum_val'].\
    mask(~cond, countries_value['total_value'].cumsum())

print(countries_value)

# it looks cool, but better to separate the df into two!
