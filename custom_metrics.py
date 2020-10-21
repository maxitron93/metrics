import math
import statistics

# P@k
def p_at_k(k, predictions, actuals):

    # Check that k is greater than 0
    if k <= 0:
        print('k must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions) != len(actuals):
        print('List lengths do not match')
        return
    
    # Calculate precision of each instance
    precisions = []
    for i in range(len(actuals)):
        TP = 0
        FP = 0
        for prediction in predictions[i][:k]:
            if prediction in actuals[i]:
                TP += 1
            else:
                FP += 1
        instance_precision = TP / (TP + FP)
        precisions.append(instance_precision)
    
    # Calculate overall precision
    precision = sum(precisions) / len(precisions)
    
    # Return precision
    return(precision)

# nR@k
def nr_at_k(k, predictions, actuals):

    # Check that k is greater than 0
    if k <= 0:
        print('k must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions) != len(actuals):
        print('List lengths do not match')
        return

    # Calculate nR of each instance
    nRs = []
    for i in range(len(actuals)):
        recall_count = 0
        for prediction in predictions[i][:k]:
            if prediction in actuals[i]:
                recall_count += 1
        maximum_possible_recall_count = len(actuals[:k])
        normalized_recall = recall_count / maximum_possible_recall_count
        nRs.append(normalized_recall)

    # Calculate overall nR
    nR = sum(nRs) / len(nRs)
    
    # Return nR
    return(nR)

# nDCG@k
def ndcg_at_k(k, predictions, actuals):

    # Check that k is greater than 0
    if k <= 0:
        print('k must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions) != len(actuals):
        print('List lengths do not match')
        return
    
    # Calculate ndcg of each instance
    nDCGs = []
    for i in range(len(actuals)):
        instance_DCG = 0
        
        # Calculate DCG
        position_counter = 0
        for prediction in predictions[i][:k]:
            position_counter += 1
            if prediction in actuals[i]:
                instance_DCG += 1 / math.log2(position_counter + 1)

        # Calculate best possible DCG
        best_possible_DCG = 0
        position_counter = 0
        for actual in actuals[i][:k]:
            position_counter += 1
            best_possible_DCG += 1 / math.log2(position_counter + 1)

        # Calculate nDCG
        instance_nDCG = instance_DCG / best_possible_DCG
        nDCGs.append(instance_nDCG)

    # Calculate overall nDCG
    nDCG = sum(nDCGs) / len(nDCGs)

    # Return nDCG
    return(nDCG)

# p_at_k_by_decile
def p_at_k_by_decile(k, predictions_by_decile, actuals_by_decile):

    # Check that k is greater than 0
    if k <= 0:
        print('k must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions_by_decile) != len(actuals_by_decile):
        print('List lengths do not match')
        return

    # Calculate precision by decile of each instance
    precisions = {10: [], 9:[], 8:[], 7:[], 6:[], 5:[], 4:[], 3:[], 2:[], 1:[], 'not_included':[]}
    for i in range(len(actuals_by_decile)):
        for decile, pred_array in predictions_by_decile[i].items():
            
            # Only perform calculation if there are actual labels in this decile
            if len(actuals_by_decile[i][decile]) > 0:
                TP = 0
                FP = 0
                preds = pred_array[:k]
                for pred in preds:
                    if pred in actuals_by_decile[i][decile]:
                        TP += 1
                    else:
                        FP += 1
                if TP + FP == 0: # If no predictions are made for this decile, return precision = 0
                    instance_precision_for_this_decile = 0
                else:
                    instance_precision_for_this_decile = TP / (TP + FP)
                precisions[decile].append(instance_precision_for_this_decile)
    
    # Calculate overall precision for each decile
    precision_by_decile = {}
    for decile, precisions_arr in precisions.items():
        precision_by_decile[decile] = sum(precisions_arr) / len(precisions_arr)

    # Return precision_by_decile
    return(precision_by_decile)

# ndcg_at_k_by_decile
def nDCG_at_k_by_decile(k, predictions_by_decile, actuals_by_decile):

    # Check that k is greater than 0
    if k <= 0:
        print('k must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions_by_decile) != len(actuals_by_decile):
        print('List lengths do not match')
        return

    # Calculate ndcg by decile of each instance
    nDCGs = {10: [], 9:[], 8:[], 7:[], 6:[], 5:[], 4:[], 3:[], 2:[], 1:[], 'not_included':[]}
    for i in range(len(actuals_by_decile)):
        for decile, pred_array in predictions_by_decile[i].items():
            
            # Only perform calculation if there are actual labels in this decile
            if len(actuals_by_decile[i][decile]) > 0:
                
                # Calculate instance_DCG_for_this_decile
                instance_DCG_for_this_decile = 0
                preds = pred_array[:k]
                position_counter = 0
                for pred in preds:
                    position_counter += 1
                    if pred in actuals_by_decile[i][decile]:
                        instance_DCG_for_this_decile += 1 / math.log2(position_counter + 1)
                
                # Calculate best_possible_DCG_for_this_decile
                best_possible_DCG_for_this_decile = 0
                position_counter = 0
                for actual in actuals_by_decile[i][decile][:k]:
                    position_counter += 1
                    best_possible_DCG_for_this_decile += 1 / math.log2(position_counter + 1)

                # Calculate instance_nDCG_for_this_decile
                instance_nDCG_for_this_decile = instance_DCG_for_this_decile / best_possible_DCG_for_this_decile
                nDCGs[decile].append(instance_nDCG_for_this_decile)

    # Calculate overall nDCG for each decile
    nDCG_by_decile = {}
    for decile, nDCGs_arr in nDCGs.items():
        nDCG_by_decile[decile] = sum(nDCGs_arr) / len(nDCGs_arr)

    # Return precision_by_decile
    return(nDCG_by_decile)

# median_k_for_recall
def median_k_for_recall(min_recall, predictions_by_decile, actuals_by_decile, num_unique_labels):

    # Check that min_recall is greater than 0
    if min_recall <= 0:
        print('min_recall must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions_by_decile) != len(actuals_by_decile):
        print('List lengths do not match')
        return

    # Calculate k_for_recall by decile for each instance
    ks_for_recall = {10: [], 9:[], 8:[], 7:[], 6:[], 5:[], 4:[], 3:[], 2:[], 1:[], 'not_included':[]}
    for i in range(len(predictions_by_decile)):
        for decile, pred_array in predictions_by_decile[i].items():

            # Only perform calculation if there are actual labels in this decile
            if len(actuals_by_decile[i][decile]) > 0:

                k = 0
                TP = 0
                for pred in pred_array:
                    k += 1
                    if pred in actuals_by_decile[i][decile]:
                        TP += 1
                    # Append k and break out of the loop as soon as min_recall is reached
                    if (TP / len(actuals_by_decile[i][decile])) >= min_recall: 
                        ks_for_recall[decile].append(k)
                        break
                    # Append half the number of unique labels if all the predictions are exhausted before min_recall is reached
                    if k == len(pred_array): 
                        ks_for_recall[decile].append(num_unique_labels // 2)

    # Calculate median_k_for_recall for each decile
    median_k_for_recall_by_decile = {}
    for decile, ks_arr in ks_for_recall.items():
        median_k_for_recall_by_decile[decile] = statistics.median(ks_arr)
    
    # Return precision_by_decile
    return(median_k_for_recall_by_decile)

# mean_k_for_recall
def mean_k_for_recall(min_recall, predictions_by_decile, actuals_by_decile, num_unique_labels):

    # Check that min_recall is greater than 0
    if min_recall <= 0:
        print('min_recall must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions_by_decile) != len(actuals_by_decile):
        print('List lengths do not match')
        return

    # Calculate k_for_recall by decile for each instance
    ks_for_recall = {10: [], 9:[], 8:[], 7:[], 6:[], 5:[], 4:[], 3:[], 2:[], 1:[], 'not_included':[]}
    for i in range(len(predictions_by_decile)):
        for decile, pred_array in predictions_by_decile[i].items():

            # Only perform calculation if there are actual labels in this decile
            if len(actuals_by_decile[i][decile]) > 0:

                k = 0
                TP = 0
                for pred in pred_array:
                    k += 1
                    if pred in actuals_by_decile[i][decile]:
                        TP += 1
                    # Append k and break out of the loop as soon as min_recall is reached
                    if (TP / len(actuals_by_decile[i][decile])) >= min_recall: 
                        ks_for_recall[decile].append(k)
                        break
                    # Append half the number of unique labels if all the predictions are exhausted before min_recall is reached
                    if k == len(pred_array):
                        ks_for_recall[decile].append(num_unique_labels // 2)

    # Calculate mean_k_for_recall for each decile
    mean_k_for_recall_by_decile = {}
    for decile, ks_arr in ks_for_recall.items():
        mean_k_for_recall_by_decile[decile] = statistics.mean(ks_arr)

    # Return precision_by_decile
    return(mean_k_for_recall_by_decile)

# prediction_proportions_at_k
def prediction_proportions_at_k(k, predictions, label_decile_mapping):

    # Check that k is greater than 0
    if k <= 0:
        print('k must be greater than 0')
        return
    
    # Assign each prediction into its decile 
    prediction_counts_by_decile = {10: 0, 9: 0, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 'not_included': 0}
    for pred_set in predictions:
        for pred in pred_set[:k]:
            try:
                prediction_counts_by_decile[label_decile_mapping[pred]] += 1
            except:
                prediction_counts_by_decile['not_included'] += 1
    
    # For each decile, calculate the predictions as a proportion of total predictions made
    prediction_proportions_by_decile = {10: 0, 9: 0, 8: 0, 7: 0, 6: 0, 5: 0, 4: 0, 3: 0, 2: 0, 1: 0, 'not_included': 0}
    for decile, count in prediction_counts_by_decile.items():
        proportion = count / (k * len(predictions))
        prediction_proportions_by_decile[decile] = proportion

    return(prediction_proportions_by_decile)

# positive_coverage_at_k
def positive_coverage_at_k(k, predictions, actuals, label_decile_mapping):

    # Check that k is greater than 0
    if k <= 0:
        print('k must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions) != len(actuals):
        print('List lengths do not match')
        return

    # Check for correct predictions by decile
    correct_predictions_by_decile = {10: [], 9: [], 8: [], 7: [], 6: [], 5: [], 4: [], 3: [], 2: [], 1: []}
    for i in range(len(predictions)):
        for pred in predictions[i][:k]:
            if pred in actuals[i]:
                decile = label_decile_mapping[pred]
                correct_predictions_by_decile[decile].append(pred) # Append every correct prediction to its decile list
            
    # Create correctly predicted labels unique by decile:
    currectly_predicted_labels_uniqe_by_decile = {}
    for decile, correct_predictions_list in correct_predictions_by_decile.items():
        currectly_predicted_labels_uniqe_by_decile[decile] = list(set(correct_predictions_list))

    # Count the number of uniqe labels in each decile
    num_unique_labels_by_decile = {}
    for label, decile in label_decile_mapping.items():
        try:
            num_unique_labels_by_decile[decile] += 1
        except:
            num_unique_labels_by_decile[decile] = 1

    # Calculate positive coverage by decile
    positive_coverage_by_decile = {}
    for decile, unique_labels_list in currectly_predicted_labels_uniqe_by_decile.items():
        num_uniqe_labels_for_this_decile = len(unique_labels_list)
        total_uniqe_labels_for_this_decile = num_unique_labels_by_decile[decile]
        positive_coverage_for_this_decile = num_uniqe_labels_for_this_decile / total_uniqe_labels_for_this_decile
        positive_coverage_by_decile[decile] = positive_coverage_for_this_decile

    return(positive_coverage_by_decile)
            
# overall_positive_coverage
def overall_positive_coverage(k, predictions, actuals):

    # Check that k is greater than 0
    if k <= 0:
        print('k must be greater than 0')
        return
    
    # Check that the list sizes match
    if len(predictions) != len(actuals):
        print('List lengths do not match')
        return

    # Check for correct predictions
    correct_predictions = []
    for i in range(len(predictions)):
        for pred in predictions[i][:k]:
            if pred in actuals[i]:
                correct_predictions.append(pred)
    
    # Get set of correct predictions
    labels_with_positive_coverage = list(set(correct_predictions))

    # Get number of unique labels
    actual_labels = []
    for actual_set in actuals:
        for actual in actual_set:
            actual_labels.append(actual)
    num_unique_labels = len(list(set(actual_labels)))

    # Calculate proportion of labels with positive coverage
    positive_coverage = len(labels_with_positive_coverage) / num_unique_labels

    return(positive_coverage)
