

import pandas as pd

df = pd.read_csv('data.csv')

###data prep

df['gas_price']=df['gas_price']*1e-9 # in gwei
df['gas_limit']=df['gas_limit']*1e-3 # in thousands to see coefs
df['block_time']=pd.to_datetime(df['block_time'], infer_datetime_format=True) 

df['call_success']=df['call_success'].astype('int') #call success as number not bool
df['call_revert']=1-df['call_success'] #reverts are more intuitive to model

# Filter out some solvers
df = df[~df['solver'].isin(['Otex','PLM','1inch','ParaSwap','0x','Test Solver 2', 'Atlas'])]

# Filter out some batches
df= df.loc[df['block_time'] >= '2022-02-17'] #post-exclusive-flashbots-only, see the Analytics for reasoning

from .log_reg import myLogRegression

myLogiRegFinal = myLogRegression(['gas_limit','gas_price'], df, resampling=False)

intercept = myLogiRegFinal.intercept_[0]
slope_gas_limit = myLogiRegFinal.coef_[0][0]
slope_gas_price = myLogiRegFinal.coef_[0][1]

print("===== REGRESSION PARAMETERS =====")
print("      intercept (β) :\t", intercept)
print("slope_gas_limit (α1):\t", slope_gas_limit)
print("slope_gas_price (α2):\t", slope_gas_price)

