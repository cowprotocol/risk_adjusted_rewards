# Instructions

1. To download the relevant data and generate the corresponding .csv file, run
```python src/collect_data.py```

Note: you need an Etherscan and Infura API key, which you should copy in the source/config.py file.

2. To train the model, run
```python src/main.py```

3. Read value of the 4 constants β (intercept), ɑ1 (corresponding to gas_used), ɑ2 (corresponding to gas_price), and ɑ3 (corresponding to num_orders) 

# Formula

Probability of revert p is

```
p = 1/(1 + exp(-β - ɑ1 * gas_used / 10^6 - ɑ2 * gas_price / 10 - ɑ3 * num_orders)))
```

where gas_price in gwei.
