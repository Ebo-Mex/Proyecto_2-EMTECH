"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    *                                       *
    *  CÓDIGO ESCRITO POR EMMANUEL BOLAÑOS  *
    *                                       *
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

# Importamos las librerías a usar
import sys
import pandas as pd
import csv

print("BIENVENIDO!")

# Abrimos el archivo, leemos los valores y creamos una
# dataframe con ellos en la variable df
with open("synergy_logistics_database.csv", "r") as database:
    df = pd.read_csv(database, index_col=0)
    print("[INFO] Archivo csv leído")

while 1:
    print("""
                   MENÚ
    1)  VER RESULTADOS PARA LA OPCIÓN 1
    2)  VER RESULTADOS PARA LA OPCIÓN 2
    3)  VER RESULTADOS PARA LA OPCIÓN 3
    4)  VER TODO
    5)  SALIR
    """)

    menu = [1, 2, 3, 4, 5]
    op = 0

    while op not in menu:
        try:
            op = int(input("\nINGRESE SOLO EL NÚMERO DE LA OPCIÓN QUE DESEA ACCEDER: "))
        except ValueError:
            print("Ese no es un número\nVuelve a probar")

    if op == 5:
        break

    ans = ["Y", "N"]
    save = "a"
    print("\n¿QUIERES GUARDAR LOS RESULTADOS?\n")
    while save not in ans:
        save = str(input("\nINGRESA SOLO 'Y' (sí) o 'N' (no): "))
        if save not in ans:
            print("Esa no es una opción\nVuelve a probar")

    if save == "Y":
        print("GUARDANDO RESULTADOS!")
    else:
        print("NO SE GUARDARA NADA")

    if op == 1 or op == 4:
        # OP.1 RUTAS IN/OUT. Cuales son las 10 rutas con más flujo
        # Obtenemos los nombres de las columnas
        # y los asignamos a una variable
        cols = df.columns

        # Tomamos las columnas que nos interesan para realizar
        # el análisis propuesto en la opción 1
        util_cols_1 = [cols[0], cols[1], cols[2], cols[8]]

        # Filtramos la df para solo mostrar las columnas
        # que nos interesan
        df_op1 = df.loc[:, util_cols_1]

        # Agrupamos con groupby las filas donde la columna de dirección,
        # origen y destino coinciden. Además, usando las funciones sum, count y mean
        # calculamos el total de ganancias, la cantidad de veces que se ha usado la
        # ruta y el promedio lo usamos para conocer cual es la ganancia por viaje
        df_op1 = df_op1.groupby([cols[0], cols[1], cols[2]]).\
            agg(['sum', 'count', 'mean']).reset_index()

        # Calculamos la ganancia por viaje promedio. Este dato nos ayudará a filtrar
        # las rutas que no produzcan suficientes ganancias
        avg_mean = df_op1.loc[:, ('total_value', 'sum')].sum() / \
                   df_op1.loc[:, ('total_value', 'count')].sum()

        # Quitamos las rutas que no cumplan con el mínimo de ganancias
        df_op1 = (df_op1.loc[df_op1.loc[:, ('total_value', 'mean')] > avg_mean])

        # Ordenamos los valores en orden descendente, para conocer las rutas
        # que se usaron más de la tabla filtrada
        df_op1 = df_op1.sort_values([('total_value', 'count')], ascending=False)

        # Creamos una dataframe para exportaciones y otra para importaciones
        df_op1_exp = df_op1.loc[df_op1.iloc[:, 0] == 'Exports']
        df_op1_imp = df_op1.loc[df_op1.iloc[:, 0] == 'Imports']

        # Usamos slicing para seleccionar solo las primeras 10 rutas
        df_op1_exp_ans = df_op1_exp.iloc[:10, 1:]
        df_op1_imp_ans = df_op1_imp.iloc[:10, 1:]

        # Además, observamos las rutas menos usadas
        df_op1_exp_extra = df_op1_exp.iloc[-10:, 1:]
        df_op1_imp_extra = df_op1_imp.iloc[-10:, 1:]

        # Mostramos el resultado
        print('\n\nRutas de exportación más usadas\n')
        print(df_op1_exp_ans)
        print('\nRutas de importación más usadas\n')
        print(df_op1_imp_ans)

        # Mostramos las rutas menos usadas
        print('\n\nRutas de exportación menos usadas\n')
        print(df_op1_exp_extra)
        print('\nRutas de importación menos usadas\n')
        print(df_op1_imp_extra)
        if save == "Y":
            df_op1_exp_ans.to_csv('outputs/op_1_exp.csv')
            df_op1_imp_ans.to_csv('outputs/op_1_imp.csv')
            df_op1_exp_extra.to_csv('outputs/op_1_exp_extra.csv')
            df_op1_imp_extra.to_csv('outputs/op_1_imp_extra.csv')

    if op == 2 or op == 4:
        # OP.2 MEDIO DE TRANSPORTE. Los 3 medios mas importantes según el valor
        # de las in/out. Cual se puede reducir.
        # Obtenemos los nombres de las columnas
        # y los asignamos a una variable
        cols = df.columns

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
        max_rets = max_rets.rename(
            columns={'sum': 'norm_sum', 'count': 'norm_count', 'mean': 'norm_mean'})

        # Agregamos los valores obtenidos a nuestra dataframe anterior
        # e imprimimos el resultado
        df_op2 = df_op2.join(max_rets)
        print('\n\nGanancias por medio de transporte\n')
        print(df_op2)
        if save == "Y":
            df_op2.to_csv('outputs/op_2.csv')

    if op == 3 or op == 4:
        # OP.3 VALOR TOTAL DE IN/OUT. Si nos enfocamos en los países que generan
        # el 80% del valor de los in/outs, que países serian esos.

        # Dataframe con las sumas para cada país
        countries_totals = df.groupby(['direction', 'origin']).\
            total_value.sum().reset_index()

        # Dividir datos en dos dataframes distintos,
        # uno para exportaciones y otro para importaciones
        countries_sum_exports = (countries_totals.loc[countries_totals['direction'] == 'Exports'])
        countries_sum_imports = (countries_totals.loc[countries_totals['direction'] == 'Imports'])

        # Dividir las sumas de cada país entre la suma total
        # y agregar como una nueva columna
        countries_per_export = (countries_sum_exports.iloc[:, 2]
                                / countries_sum_exports.iloc[:, 2].sum()).rename('total_%')
        countries_per_import = (countries_sum_imports.iloc[:, 2]
                                / countries_sum_imports.iloc[:, 2].sum()).rename('total_%')

        # Agregamos los porcentajes obtenidos a su respectivo dataframe
        countries_sum_exports = pd.concat([countries_sum_exports, countries_per_export], axis=1)
        countries_sum_imports = pd.concat([countries_sum_imports, countries_per_import], axis=1)

        # Ordenamos ambos dataframes en orden descendente
        countries_sum_exports.sort_values(['total_%'], ascending=False, inplace=True)
        countries_sum_imports.sort_values(['total_%'], ascending=False, inplace=True)

        # Hacemos una suma acumulativa, de esta forma conoceremos los países
        # que generan el 80% de los ingresos
        countries_sum_exports['cumulative_%'] = countries_sum_exports['total_%'].cumsum()
        countries_sum_imports['cumulative_%'] = countries_sum_imports['total_%'].cumsum()

        # Filtramos las datasets para mostrar solo las que están dentro del limite
        countries_sum_exports = countries_sum_exports.loc[countries_sum_exports['cumulative_%'] <= 0.8]
        countries_sum_imports = countries_sum_imports.loc[countries_sum_imports['cumulative_%'] <= 0.8]

        # Mostramos el resultado
        print('\n\n Lista de países exportadores que aportan al 80% de ganancias\n')
        print(countries_sum_exports)
        print('\n Lista de países importadores que aportan al 80% de ganancias\n')
        print(countries_sum_imports)
        if save == "Y":
            countries_sum_exports.to_csv('outputs/op_3_exp.csv')
            countries_sum_imports.to_csv('outputs/op_3_imp.csv')
