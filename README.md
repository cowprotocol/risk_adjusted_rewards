# Instructions

1. Run this query https://dune.com/queries/1253760 and download results as data.csv

NOTE: It would be great to get this data from our DB instead, but it is not easy to see if a tx reverted or not.

2. python -m src.main

3. Read value of the 3 constants ɑ1, ɑ2, and β 

# Formula

Probability of revert p is

```
p = 1/(1 + exp(-β - ɑ1 * gas_used / 10^6 - ɑ2 * gas_price / 10 - ɑ3 * num_orders)))
```

where gas_price in gwei.
