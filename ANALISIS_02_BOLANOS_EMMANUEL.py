import pandas as pd
import numpy as np

with open("synergy_logistics_database.csv", "r") as database:
    df = pd.read_csv(database, index_col=0)

# OP.1 RUTAS IN/OUT. Deberíamos enfocarnos en las 10 rutas mas demandadas.

cols = df.columns
print(cols)

util_cols = [cols[0], cols[1], cols[2]]

df = df.loc[:, util_cols]

df = df.groupby(util_cols).size().reset_index()

#print(df.head())

# cols = ['direction', 'origin', 'destination', 'total_value']
#
# df = (df.loc[:, cols]).set_index([cols[0], cols[1]])
#
# for og, frame in df.groupby('origin'):
#     total_sum = np.sum(frame['total_value'])
#     print(og + " has a total value of " + str(total_sum))

# OP.2 MEDIO DE TRANSPORTE. Los 3 medios mas importantes segun el valor
# de las in/out. Cual se puede reducir.
# OP.3 VALOR TOTAL DE IN/OUT. Si nos enfocamos en los paises que generan
# el 80% del valor de los in/outs, que paises serian esos.
