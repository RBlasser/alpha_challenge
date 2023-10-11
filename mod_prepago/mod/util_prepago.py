# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 11:57:29 2023

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




class TablaPrepago:
    
    def __init__(self,
                 df,
                 strCredito,
                 interest_rate, 
                 flt_pagos_periodo,  
                 principal,  
                 start_date, 
                 end_date, 
                 strProducto,
                 str_Fecha_Proceso, 
                 payments_year_cap,
                 frecuency_cap,
                 flt_pagos_periodo_cap,
                 strPeriodicidad_intereses,
                 strPeriodicidad_capital,
                 flt_califcred):
        
        self.df = df
        self.strCredito = strCredito
        self.interest_rate = interest_rate/12
        self.flt_pagos_periodo = flt_pagos_periodo
        self.principal = principal
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.strProducto =  strProducto
        self.str_Fecha_Proceso = pd.to_datetime(str_Fecha_Proceso)
        self.payments_year_cap =  payments_year_cap
        self.frecuency_cap = frecuency_cap
        self.flt_pagos_periodo_cap = flt_pagos_periodo_cap
        self.strPeriodicidad_intereses = strPeriodicidad_intereses
        self.strPeriodicidad_capital = strPeriodicidad_capital
        self.flt_califcred = flt_califcred
        
        self.vida_actual = int((str_Fecha_Proceso - start_date).days/30)
        self.plazo = flt_pagos_periodo
        self.letra = df['Principal'].iloc[0] + df['Interest'].iloc[0]
     
    def select_curva(self) -> str:
        
        crr = self.flt_califcred
    
        
        vida_actual = int(self.vida_actual)
        
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
            
            #print(tasa, saldo, meses_restantes, limit)
            vec = np.arange(start=0, stop=limit)
            vfun = np.vectorize(lambda i: npf.ppmt(tasa, i, meses_restantes, saldo))
            # print("\n",vfun(vec))
            # print(tasa, saldo, meses_restantes, limit)
            
            return vfun(vec)[:int(limit)]
        

    # Actualizar último flujo de capital
    global update_last_cap
    def update_last_cap(vector_cap, saldo):
        
        vector_cap[-1] = vector_cap[-1] + (saldo - sum(vector_cap))
        
        return vector_cap
    
    
    # Vector de pagos interes
    global int_vector
    def int_vector(tasa, saldo, meses_restantes, limit):
            
            vec = np.arange(start=0, stop=limit)
            vfun = np.vectorize(lambda i: npf.ipmt(tasa, i, meses_restantes, saldo))
            #print(tasa, meses_restantes, saldo)
            
            return vfun(vec)[:int(limit)]
        
        
    # Agregar prepago a flujos capital
    global add_prepago
    def add_prepago(vector, at_per, prepago):
        

        t_cap = vector[at_per]
        vector[at_per] = abs(t_cap + prepago)
        
        #print(at_per,t_cap, prepago)
        
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
    def adj_cap(vector_cap, vector_int, letra, pers_prep):
        
        a1 = vector_cap
        a2 = vector_int
        
        for i, each_i in enumerate(zip(a1, a2)):
            
            pmt0 = round(sum(each_i), 4)
            
            # print("pagoCap {} | pagoInt {} | pago {}".format(i, each_i, pmt0))
            
            if pmt0 != round(letra,4) and (i+1) not in pers_prep:
                #print(a1[i], pmt0)
                adj_0 = round(letra - sum(each_i),4)
                a1[i] = round(each_i[0] + adj_0,4)                
                
            else:
                # print(i+1)
                #print("\t No aplica",a1[i], pmt0)
                pass
                
                
        return a1 #vector_cap
    
    # Constructor
    def builder(self) -> pd.DataFrame:
        
        id_ = self.strCredito
        freq_int = self.strPeriodicidad_intereses
        freq_cap = self.strPeriodicidad_capital
        saldo = self.principal
        tasa = self.interest_rate
        crr = self.flt_califcred
        vida_actual = self.vida_actual
        plazo = self.plazo
        
        curva = df_curvas[(df_curvas['Curva']==self.select_curva())&(df_curvas['Match'].str.startswith('HIPOTECAS'))].reindex(columns=['Meses', 'Prob'])
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
        main_cap = np.array(self.df['Principal'])
        
        # Periodos donde hay prepago
        self.pers_prep = dx[dx['Prob']>0]['Per'].to_list()
        
        
        vector_id = []
        flujos_interes = []
        saldos = []
        
        saldos_pagos = []
        
        cur_saldo = saldo
        prepagos = []
        for index, row in params.iterrows():  
        
            if cur_saldo <=1:
                
                pass
                #print(cur_saldo)
            
            else:
                
                pagos_capital = sum(cap_vector(tasa, cur_saldo, row['meses_restantes'], row['limit_array']))
                vector_interes = int_vector(tasa, cur_saldo, row['meses_restantes'], row['limit_array'])
                
                
                if row['Prob'] > 0:
                    #prepago = (saldo + pagos_capital) * (1 - row['Prob'])
                    prepago = (cur_saldo + pagos_capital) * (1 - row['Prob'])
                    
                    saldos_pagos.append([cur_saldo, pagos_capital, 1 - row['Prob'] ])
                    prepagos.append(prepago)
                
                else:
                    prepago = 0
                
                
                cur_saldo = cur_saldo + pagos_capital - prepago
                main_cap = add_prepago(main_cap, int(row['mes_prepago']) - 1, prepago)
                
                vector_id.append(id_)
                flujos_interes.append(vector_interes)
                saldos.append(cur_saldo)
                
                #print(index, pagos_capital, cur_saldo, prepago)
                
        int_concat = abs(np.concatenate(flujos_interes))
        
        # Flujos Capital ajustados
        adj_cap(main_cap, int_concat, self.letra, self.pers_prep)
        
        
        # Actualizar Flujos 
        di = self.df.copy()
        di = di.drop(columns=di.columns[0])
        di = di.iloc[:update_bal(main_cap, saldo)]
        di['Principal'] = pd.Series(update_last_cap(main_cap[:update_bal(main_cap, saldo)], self.principal))
        #di['Interest'] =  pd.Series(int_concat).iloc[:update_bal(main_cap, saldo)]
        di['Interest'] =  pd.Series(int_concat).iloc[:update_bal(main_cap, saldo)+1]
        di['Payment'] = di['Principal'] + di['Interest']
        
        
        return di
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    