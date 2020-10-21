# Metrics for Minor Thesis

## P@k
Calculates the precision given the top k predictions

TP = number of predicted labels that are in set of actual labels
FP = number predicted labels that are <strong>not</strong> in set of actual labels

precision for each instance = TP / (TP + FP)

#### P@k = sum(precision for each instance) / (number of instances)

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

#### nDCG@k = sum(nDCG for each instance) / (number of instances)

## p_at_k_by_decile
Calculates the precision given the top k predictions for each decile

1) every predicion in the top 500 predictions is placed in their decile
e.g. prediction_set = {10: [0, 1], 9: [5, 11], 8: [30, 56], ..., 1: [3640, 3640, ...]}

2) every label in the set of actual labels is placed in their decile
e.g. actual_set = {10: [1], 9: [], 8: [12], ..., 1: [2547]}

3) precision is calculated at each decile for top k predicions using the formula for P@k above. If there are no actual labels in the decile, then skip the calculation. If there are no predictions at the decile, then precision is 0.

#### P@k for each decile = sum(all calculated instance precision at the decile) / (number of calculated precisions at that decile)

## nDCG_at_k_by_decile
Calculates the nDCG given the top k predictions for each decile

Same steps as p_at_k_by_decile, but calculates nDCG instead of precision

## median_k_for_recall
Calculates the median k predictions required to achieve min_recall at each decile

1) every predicion in the top 500 predictions is placed in their decile
e.g. prediction_set = {10: [0, 1], 9: [5, 11], 8: [30, 56], ..., 1: [3640, 3640, ...]}

2) every label in the set of actual labels is placed in their decile
e.g. actual_set = {10: [1], 9: [], 8: [12], ..., 1: [2547]}

3) Itterate through each list of predictions until min_recall is reached, and return that k value for each decile. If min_recall isn't achieved before running out of predictions, return k as half of the number of unique labels.

#### median_k_for_recall = The median returned k value for each decile

## mean_k_for_recall
Calculates the mean k predictions required to achieve min_recall at each decile

Same steps as median_k_for_recall above but calculates mean instead of median

## prediction_proportions_at_k
Calculates the proportion of predictions that belong to each decile given the top k predictions

1) Given the top k predictions for the test set, count the number predictions that fall into each decile
e.g. {10: 1637, 9: 1372, 8: 572, ..., 1: 63}

2) Calculate the total number of predictions made as k * (number of test instances)

#### prediction_proportions_at_k = divide the count at each decile by the total number of predictions made

## positive_coverage_at_k
Calculates the proportion of uniqe labels that have at least one correct prediction given the top k predictions

1) every predicion in the top k predictions is placed in their decile
e.g. prediction_set = {10: [0, 1], 9: [5, 11], 8: [30, 56], ..., 1: [3640, 3640, ...]}

2) every label in the set of actual labels is placed in their decile
e.g. actual_set = {10: [1], 9: [], 8: [12], ..., 1: [2547]}

3) Itterate through the predictions and check if the prediction is correct. Append every correct prediction to a list of correctly predicted labels

4) Pass the list of correctly predicted labels through a set() function

5) Using the set of actual labels, count the number of unique labels at each decile

#### positive_coverage_by_decile = (count of correctly predicted unique labels at each decile) / (number of unique labels at each decile)

