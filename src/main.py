import pandas as pd

fileName = input("Enter input csv file: ")
df = pd.read_csv(fileName)

###data prep
df['success']=df['success'].astype('int') #call success as number not bool
df['revert']=1-df['success'] #reverts are more intuitive to model

from log_reg import myLogRegression

myLogiRegFinal = myLogRegression(['gas_used','gas_price','num_orders'], df, resampling=False)

intercept = myLogiRegFinal.intercept_[0]
slope_gas_used = myLogiRegFinal.coef_[0][0]
slope_gas_price = myLogiRegFinal.coef_[0][1]
slope_num_orders = myLogiRegFinal.coef_[0][2]


print("===== REGRESSION PARAMETERS =====")
print("      intercept (β) :\t", intercept)
print("slope_gas_used (α1):\t", slope_gas_used)
print("slope_gas_price (α2):\t", slope_gas_price)
print("slope_numb_orders (α3):\t", slope_num_orders)

