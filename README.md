# Metrics for Minor Thesis


## P@k
Calculates the precision given the top k predictions

TP = number of predicted labels that are in set of actual labels
FP = number predicted labels that are <strong>not</strong> in set of actual labels

precision for each instance = TP / (TP + FP)

P@k = (precision for each instance) / (number of instances)

## nR@k
Calculates normalized recall given the top k predictions

Not important - turns out to be exactly the same as P@k

## nDCG@k
Calculates normalized discounted cumulative gain given the top k predictions

for every correctly preicted label in set of <strong>predicted</strong> labels:
DCG += 1 / math.log2(position_counter + 1)

for every label in set of <strong>actual</strong> labels:
Best possible DCG += 1 / math.log2(position_counter + 1)

nDCG for each instance = (DCG) / (Best possible DCG)

nDCG@k = (nDCG for each instance) / (number of instances)
