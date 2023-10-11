# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:32:45 2023

@author: rblasser
"""

import os
import pandas as pd
import numpy as np
import numpy_financial as npf

import warnings
warnings.filterwarnings("ignore")

# DIRS
dir_IN =  r'\\NTAPPAMA01-C01\Market Risk\RIESGO ML\LIBRO BANCARIO\TASA DE INTERES\OTROS\Modelo_valoracion_cartera_prepago\0_INPUT'


# Curvas
df_curvas = pd.read_excel(os.path.join(dir_IN, "Curvas_Prepago.xlsx"))
df_curvas = df_curvas.reindex(columns=("años", "Meses", "Curva", "CRR", "Carteras_prepago", "Match", "Key", "Prob"))



def select_curva(crr, vida_actual) -> str:
    
    #crr = self.flt_califcred
    #vida_actual = int(self.vida_actual)
    
    
    if crr == 1 and 0 <= vida_actual <= 43:	
        return 'VD_VVDA_0_43_C1_PREPAGOS'
    
    if crr == 1 and 44 <= vida_actual <= 149:	
        return 'VD_VVDA_44_149_C1_PREPAGOS'
    
    if crr == 1 and   vida_actual >= 150:	
        return 'VD_VVDA_150_C1_PREPAGOS'
    
    if crr == 2 and 0 <= vida_actual <= 43:	
        return 'VD_VVDA_0_43_C2_PREPAGOS'
   
    if crr == 2 and 44 <= vida_actual <= 149:	
        return 'VD_VVDA_44_149_C2_PREPAGOS'
    
    if crr == 2 and   vida_actual >= 150:	
        return 'VD_VVDA_150_C2_PREPAGOS'
    
    if crr == 3 and 0 <= vida_actual <= 43:	
        return 'VD_VVDA_0_43_C3_PREPAGOS'
    
    if crr == 3 and 44 <= vida_actual <= 149:	
        return 'VD_VVDA_44_149_C3_PREPAGOS'
    
    if crr == 3 and   vida_actual >= 150:	
        return 'VD_VVDA_150_C3_PREPAGOS'
    
    if crr == 4 and 0 <= vida_actual <= 43:	
        return 'VD_VVDA_0_43_C4_PREPAGOS'
    
    if crr == 4 and 44 <= vida_actual <= 149:	
        return 'VD_VVDA_44_149_C4_PREPAGOS'
    
    if crr == 4 and   vida_actual >= 150:	
        return 'VD_VVDA_150_C4_PREPAGOS'
    
    if crr == 5 and 0 <= vida_actual <= 43:	
        return 'VD_VVDA_0_43_C5_PREPAGOS'
    
    if crr == 5 and 44 <= vida_actual <= 149:	
        return 'VD_VVDA_44_149_C5_PREPAGOS'
    
    if crr == 5 and   vida_actual >= 150:	
        return 'VD_VVDA_150_C5_PREPAGOS'
    
    if crr == 6 and 0 <= vida_actual <= 43:	
        return 'VD_VVDA_0_43_C6_PREPAGOS'
    
    if crr == 6 and 44 <= vida_actual <= 149:	
        return 'VD_VVDA_44_149_C6_PREPAGOS'
    
    if crr == 6 and   vida_actual >= 150:	
        return 'VD_VVDA_150_C6_PREPAGOS'
    
    if crr == 7 and 0 <= vida_actual <= 43:	
        return 'VD_VVDA_0_43_C7_PREPAGOS'
    
    if crr == 7 and 44 <= vida_actual <= 149:	
        return 'VD_VVDA_44_149_C7_PREPAGOS'
    
    if crr == 7 and   vida_actual >= 150:	
        return 'VD_VVDA_150_C7_PREPAGOS'
    
    


# Vector de pagos capital
global cap_vector
def cap_vector(tasa, saldo, meses_restantes, limit):
        
        # Editado RBA 20231003
        #vec = np.arange(start=0, stop=limit)
        
        meses_restantes = meses_restantes + 1 if meses_restantes <= 1 else meses_restantes
        limit = limit + 1 if limit <= 1 else limit
        
        vec = np.arange(start=1, stop=limit)
        
    
        
        vfun = np.vectorize(lambda i: npf.ppmt(tasa, i, meses_restantes, saldo))
        
        return vfun(vec)[:int(limit)]
    
    
    
# Actualizar último flujo de capital
global update_last_cap
def update_last_cap(vector_cap, saldo):
    
    vector_cap[-1] = vector_cap[-1] + (saldo - sum(vector_cap))
    
    return vector_cap


# Vector de pagos interes
global int_vector
def int_vector(tasa, saldo, meses_restantes, limit):
        
        # Editado RBA 20231003
        #vec = np.arange(start=0, stop=limit)
        vec = np.arange(start=1, stop=limit)
        
        meses_restantes = meses_restantes + 1 if meses_restantes <= 1 else meses_restantes
        limit = limit + 1 if limit <= 1 else limit

        
        vfun = np.vectorize(lambda i: npf.ipmt(tasa, i, meses_restantes, saldo))
        #print(tasa, meses_restantes, saldo)
        
        return vfun(vec)[:int(limit)]
    
    
# Agregar prepago a flujos capital
global add_prepago
def add_prepago(vector, at_per, prepago):
    

    t_cap = vector[at_per]
    vector[at_per] = abs(t_cap + prepago)
    
    #print(at_per,t_cap, prepago)
    print(at_per)
    
    return vector


# Evaluar último pago de capital nuevo (cuando el balance empieza a ser negativo)
global update_bal
def update_bal(vector, bal0):
    bal = bal0
    res = []
    for i in range(len(vector)):
        bal = bal - vector[i]
        if bal < 0:
            res.append(i)
            break
            
    return res[0] + 1


# Ajustar flujo capital para que coincida pago total
global adj_cap
def adj_cap(vector_cap, vector_int, letra, pers_prep, cur_saldo, prob, row_per):
    
    a1 = vector_cap
    a2 = vector_int
    
    for i, each_i in enumerate(zip(a1, a2)):
        
        pmt0 = round(sum(each_i), 4)

        # adj_0 = round(letra - sum(each_i),4)
        adj_0 = round(letra - pmt0, 4)
        a1[i] = round(each_i[0] + adj_0,4)  
        
        
        
        """"
        print("letra inicial {} | ajuste {} | capital ajustado {} | letra ajustada {}".format(pmt0, 
                                                                                              adj_0, 
                                                                                              a1[i], 
                                                                                              a1[i] + a2[i]))  
        """                        
          
    #print(a1)       
    return a1 #vector_cap  
    
    
####################
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

########################   
vida_actual = int((pd.to_datetime(str_Fecha_Proceso) - pd.to_datetime(start_date)).days/30)
plazo = flt_pagos_periodo
letra = df['Principal'].iloc[0] + df['Interest'].iloc[0]
id_  = strCredito 
crr = flt_califcred
    

curva = df_curvas[(df_curvas['Curva']==select_curva(crr,vida_actual))&(df_curvas['Match'].str.startswith('HIPOTECAS'))].reindex(columns=['Meses', 'Prob'])
curva['Dias'] = curva['Meses'] #*30


dx = pd.DataFrame(np.arange(start=0, stop=plazo +1), columns=['Per'])
dx['ID'] = id_
dx['Per_curr'] = dx['Per'] + vida_actual


dx = dx.merge(curva[['Dias','Prob']], left_on='Per_curr', right_on='Dias', how='left').fillna(0)
dx['Prob'] = dx['Prob'].astype(float)


params = dx[dx['Dias']!=0].reindex(columns=['Per', 'Per_curr', 'Prob'])
params.loc[0] = [0, vida_actual, 0]


params = params.sort_index()
params = params.reset_index()
    
    
mes_prepago = params[['index','Prob']].iloc[1:].reset_index().drop(columns=['level_0'])

params = params.merge(mes_prepago, right_index=True, left_index=True, how='left').drop(columns=['index_x','Prob_x']).fillna(0)
params = params.rename(columns={'index_y':'mes_prepago','Prob_y':'Prob'})
params['meses_restantes'] = plazo - params['Per']
params['limit_array'] = params['mes_prepago'] - params['Per']
params['limit_array'] = params['limit_array'].astype(int)
params.at[params.shape[0]-1, 'limit_array'] = params.at[params.shape[0]-1, 'meses_restantes'] 

# Ajustar params en cero
params['meses_restantes'] = params['meses_restantes'].apply(lambda row: 1 if row <1 else row)
params['limit_array'] = params['limit_array'].apply(lambda row: 1 if row <1 else row)

    
  
# Vector Capital proveniente del parámetro inicial
main_cap = np.array(df['Principal'])

# Periodos donde hay prepago
pers_prep = dx[dx['Prob']>0]['Per'].to_list()    
  

# Builder
id_ = strCredito
freq_int = strPeriodicidad_intereses
freq_cap = strPeriodicidad_capital
saldo = principal
tasa = interest_rate/12
crr = flt_califcred
vida_actual = vida_actual
plazo = plazo


# Listas
vector_id = []
flujos_interes = []
saldos = []
saldos_pagos = []
cur_saldo = saldo
prepagos = []


PAGOS_CAPITAL = []


for index, row in params.iterrows():  

    if cur_saldo <=1:
        
        pass
    
    else:
        
        vec_pagos_capital = cap_vector(tasa, cur_saldo, row['meses_restantes'], row['limit_array']+1)
                
        
        pagos_capital = sum(vec_pagos_capital)
        
        vector_interes = int_vector(tasa, cur_saldo, row['meses_restantes'], row['limit_array']+1)
        
        vec_pagos_capital = adj_cap(abs(vec_pagos_capital), abs(vector_interes), letra, pers_prep, cur_saldo, row['Prob'], row['mes_prepago'])
        
        
        if row['Prob'] > 0:
            prepago = (cur_saldo + pagos_capital) * (1 - row['Prob'])
            
            saldos_pagos.append([cur_saldo, pagos_capital, 1 - row['Prob'] ])
            prepagos.append(prepago)
            print(vec_pagos_capital)
            vec_pagos_capital[-1] = prepago #+ vec_pagos_capital[-1]
            
        
        else:
            prepago = 0
        
        
        cur_saldo = cur_saldo - sum(vec_pagos_capital)#- abs(pagos_capital) - prepago
        print("\n")
        print(cur_saldo)
        
        PAGOS_CAPITAL.append(vec_pagos_capital)
        
        
        
        vector_id.append(id_)
        flujos_interes.append(vector_interes)
        saldos.append(cur_saldo)
        
        # if index == 2:
        #     break
        


        
int_concat = abs(np.concatenate(flujos_interes))
cap_concat = abs(np.concatenate(PAGOS_CAPITAL))

# Flujos Capital ajustados
#adj_cap(main_cap, int_concat, letra, pers_prep)
    

# Actualizar Flujos 
di = df.copy()
di = di.drop(columns=di.columns[0])
di = di.iloc[:update_bal(cap_concat, saldo)] #['Principal'].sum()

di['Principal'] = pd.Series(cap_concat)
di['Interest'] =  pd.Series(int_concat)


di['Principal'] = pd.Series(update_last_cap(cap_concat[:update_bal(cap_concat, saldo)], principal))



#di['Interest'] =  pd.Series(int_concat).iloc[:update_bal(main_cap, saldo)]
#di['Interest'] =  pd.Series(int_concat).iloc[:update_bal(cap_concat, saldo)+1]
di['Payment'] = di['Principal'] + di['Interest']

  

  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    