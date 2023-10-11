# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 15:55:34 2023

@author: rblasser
"""

import pandas as pd

df = pd.read_excel("info_prepago/detalle_1_Sub_391632.xlsx")
strCredito  =  '391632'
interest_rate = 0.0574999999999999
flt_pagos_periodo =  336
principal = 99922.25
start_date = '30 04 2015'
end_date = '7 08 2051'
strProducto ='sub'
str_Fecha_Proceso = '18 08 2023'
payments_year_cap =  12 
frecuency_cap = 1
flt_pagos_periodo_cap = 336
strPeriodicidad_intereses = 'M'
strPeriodicidad_capital = 'M'
flt_califcred = 5
###############################################################################

from mod.util_prepago import TablaPrepago

tabla_prepago = TablaPrepago(df,
                    strCredito,
                    interest_rate, 
                    flt_pagos_periodo,  
                    principal,  
                    pd.to_datetime(start_date), 
                    pd.to_datetime(end_date), 
                    strProducto,
                    pd.to_datetime(str_Fecha_Proceso), 
                    payments_year_cap,
                    frecuency_cap,
                    flt_pagos_periodo_cap,
                    strPeriodicidad_intereses,
                    strPeriodicidad_capital,
                    flt_califcred).builder()

###############################################################################

from mod.util_prepago import TablaPrepago
import pandas as pd

df = pd.read_excel("datos/detalle_sin_prepago_327435.xlsx", sheet_name='Sheet1')
strCredito  =  '327435'
interest_rate = 0.0575
flt_pagos_periodo =  392
principal = 48048.52
start_date = '16 10 2012'
end_date = '5 05 2056'
strProducto ='sub'
str_Fecha_Proceso = '18 08 2023'
payments_year_cap =  12 
frecuency_cap = 1
flt_pagos_periodo_cap = 392
strPeriodicidad_intereses = 'M'
strPeriodicidad_capital = 'M'
flt_califcred = 2

tabla_prepago = TablaPrepago(df,
                    strCredito,
                    interest_rate, 
                    flt_pagos_periodo,  
                    principal,  
                    pd.to_datetime(start_date), 
                    pd.to_datetime(end_date), 
                    strProducto,
                    pd.to_datetime(str_Fecha_Proceso), 
                    payments_year_cap,
                    frecuency_cap,
                    flt_pagos_periodo_cap,
                    strPeriodicidad_intereses,
                    strPeriodicidad_capital,
                    flt_califcred).builder()

tabla_prepago[0].to_clipboard()
tabla_prepago[1].to_clipboard()


info = TablaPrepago(df,
                    strCredito,
                    interest_rate, 
                    flt_pagos_periodo,  
                    principal,  
                    pd.to_datetime(start_date), 
                    pd.to_datetime(end_date), 
                    strProducto,
                    pd.to_datetime(str_Fecha_Proceso), 
                    payments_year_cap,
                    frecuency_cap,
                    flt_pagos_periodo_cap,
                    strPeriodicidad_intereses,
                    strPeriodicidad_capital,
                    flt_califcred)

info.select_curva()

###############################################################################
"""
1-Error al enviar el conteo total de los pagos, crédito 595232. Tema de plazos.
"""
import pandas as pd

from mod.py_util_prepago import TablaPrepago
df = pd.read_excel("info_prepago/Crédito 595232/detalle_sin_prepagoSub_595232.xlsx")

strCredito  =  '595232'
interest_rate = 0.055
flt_pagos_periodo =  358
principal = 86592.12
start_date = '2023-05-29'
end_date = '2053-06-16'
strProducto ='sub'
str_Fecha_Proceso = '2023-08-18'
payments_year_cap =  12
frecuency_cap = 1
flt_pagos_periodo_cap = 358
strPeriodicidad_intereses = 'M'
strPeriodicidad_capital = 'M'
flt_califcred = 3

tabla_prepago = TablaPrepago(df,
                    strCredito,
                    interest_rate, 
                    flt_pagos_periodo,  
                    principal,  
                    pd.to_datetime(start_date), 
                    pd.to_datetime(end_date), 
                    strProducto,
                    pd.to_datetime(str_Fecha_Proceso), 
                    payments_year_cap,
                    frecuency_cap,
                    flt_pagos_periodo_cap,
                    strPeriodicidad_intereses,
                    strPeriodicidad_capital,
                    flt_califcred).builder()

tabla_prepago.to_clipboard(index=False)

tabla_prepago[0].to_excel("tabla_prepago.xlsx")

tabla_prepago[0].to_clipboard(index=False)
tabla_prepago[-1].to_clipboard()


###############################################################################
"""
1-Error al enviar el conteo total de los pagos, crédito 595232. Tema de plazos.
"""
import pandas as pd

from mod.util_prepago_v3 import TablaPrepago
df = pd.read_excel("info_prepago/Crédito 595232/detalle_sin_prepagoSub_595232.xlsx")

strCredito  =  '595232'
interest_rate = 0.055
flt_pagos_periodo =  358
principal = 86592.12
start_date = '2023-05-29'
end_date = '2053-06-16'
strProducto ='sub'
str_Fecha_Proceso = '2023-08-18'
payments_year_cap =  12
frecuency_cap = 1
flt_pagos_periodo_cap = 358
strPeriodicidad_intereses = 'M'
strPeriodicidad_capital = 'M'
flt_califcred = 3

tabla_prepago = TablaPrepago(df,
                    strCredito,
                    interest_rate, 
                    flt_pagos_periodo,  
                    principal,  
                    pd.to_datetime(start_date), 
                    pd.to_datetime(end_date), 
                    strProducto,
                    pd.to_datetime(str_Fecha_Proceso), 
                    payments_year_cap,
                    frecuency_cap,
                    flt_pagos_periodo_cap,
                    strPeriodicidad_intereses,
                    strPeriodicidad_capital,
                    flt_califcred).builder()




tabla_prepago.to_clipboard(index=False)

tabla_prepago[0].to_excel("tabla_prepago.xlsx")

tabla_prepago[0].to_clipboard(index=False)
tabla_prepago[-1].to_clipboard()




















###############################################################################

from mod.util_prepago import TablaPrepago
import pandas as pd

"""
2-Porcentajes de prepago no coindicen por pocos decimales
3-último bucket de prepago se corre hacia arriba cuando el saldo está por agotarse. Crédito 435602

"""

df = pd.read_excel("info_prepago/Crédito 435602/detalle_sin_prepagoSub_435602.xlsx")

strCredito  =  '435602'
interest_rate = 0.0575
flt_pagos_periodo =  310
principal = 45359.46
start_date = '2016-06-17'
end_date = '2049-06-07'
strProducto ='sub'
str_Fecha_Proceso = '2023-08-18'
payments_year_cap =  12
frecuency_cap = 1
flt_pagos_periodo_cap = 310
strPeriodicidad_intereses = 'M'
strPeriodicidad_capital = 'M'
flt_califcred = 3


tabla_prepago = TablaPrepago(df,
                    strCredito,
                    interest_rate, 
                    flt_pagos_periodo,  
                    principal,  
                    pd.to_datetime(start_date), 
                    pd.to_datetime(end_date), 
                    strProducto,
                    pd.to_datetime(str_Fecha_Proceso), 
                    payments_year_cap,
                    frecuency_cap,
                    flt_pagos_periodo_cap,
                    strPeriodicidad_intereses,
                    strPeriodicidad_capital,
                    flt_califcred).builder()


tabla_prepago[0].to_clipboard()
tabla_prepago[1].to_clipboard()



s = """
[-37.81415678 -37.99534961 -38.17741066 -38.36034409 -38.54415407
-38.72884481 -38.91442052 -39.10088545 -39.28824386 -39.47650003
-39.66565826 -39.85572287]""".replace(" ", ",")


pd.Series(s.replace("\n","").replace("'","")).sum()


s = [-37.81415678,-37.99534961,-38.17741066,-38.36034409,-38.54415407-38.72884481,-38.91442052,-39.10088545,-39.28824386,-39.47650003-39.66565826,-39.85572287]

pd.Series(s).sum()



###############################################################################

from mod.util_prepago import TablaPrepago
import pandas as pd

"""
2-Porcentajes de prepago no coindicen por pocos decimales
3-último bucket de prepago se corre hacia arriba cuando el saldo está por agotarse. Crédito 435602

"""

df = pd.read_excel("info_prepago/Crédito 435602/detalle_sin_prepagoSub_435602.xlsx")

strCredito  =  '435602'
interest_rate = 0.0575
flt_pagos_periodo =  310
principal = 45359.46
start_date = '2016-06-17'
end_date = '2049-06-07'
strProducto ='sub'
str_Fecha_Proceso = '2023-08-18'
payments_year_cap =  12
frecuency_cap = 1
flt_pagos_periodo_cap = 310
strPeriodicidad_intereses = 'M'
strPeriodicidad_capital = 'M'
flt_califcred = 3


tabla_prepago = TablaPrepago(df,
                    strCredito,
                    interest_rate, 
                    flt_pagos_periodo,  
                    principal,  
                    pd.to_datetime(start_date), 
                    pd.to_datetime(end_date), 
                    strProducto,
                    pd.to_datetime(str_Fecha_Proceso), 
                    payments_year_cap,
                    frecuency_cap,
                    flt_pagos_periodo_cap,
                    strPeriodicidad_intereses,
                    strPeriodicidad_capital,
                    flt_califcred).builder()


tabla_prepago[0].to_clipboard()

















































