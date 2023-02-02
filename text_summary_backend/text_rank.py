from models import Document, Sentence
import torch
DAMPING_FACTOR = 0.15
OUTPUT_PERCENTAGE = 0.10

class noWeightException(Exception):
    pass

def construct_weight(document):
    n = len(document.sentences)
    weights = torch.zeros(n, n)
    for index1, s1 in document.sentences.items():
        for index2, s2 in document.sentences.items():
            if index1 != index2:
                weights[index1, index2] = Sentence.weight(s1, s2)
    return weights

def scoring(document):
    n = len(document.sentences)
    weights = construct_weight(document)
    # Remove any edges less than average
    total_number_of_weight = (weights > 0).float().sum(dim=1).sum()
    if total_number_of_weight == 0.0:
        raise noWeightException('No weight!')
    average_weight = weights.sum().sum() / total_number_of_weight
    weights = torch.nn.functional.relu(weights - average_weight)
    edges = (weights > 0).float()
    weights += edges * average_weight
    degrees = edges.sum(dim=1)

    # For node with no neighbor, we can divide by 1 to avoid issue of dividing 0
    degrees += (degrees == 0.0).float()
    initial_scores = weights.sum(dim=1) / degrees
    sum_of_neighbors = edges @ initial_scores
    final_scores = DAMPING_FACTOR * n + (1 - DAMPING_FACTOR) * (sum_of_neighbors / degrees)

    return final_scores



def text_rank(document):
    n = len(document.sentences)
    try:
        final_scores = scoring(document)
    except noWeightException as _:
        return document.sentences[0].original

    sorted_scores = sorted(final_scores)[::-1]
    threshold = sorted_scores[int(n * OUTPUT_PERCENTAGE)]
    # 0 needs to be treated specially here since we use a mask multiplied by torch.arange(n) to 
    # get indices, and 0 is almost always there
    includes_zero = final_scores[0] >= threshold
    selected_indices = set(((final_scores - threshold >= 0) * torch.arange(n)).int().tolist())
    if not includes_zero:
        selected_indices.remove(0)
    output = ' '.join([document.sentences[i].original for i in sorted(list(selected_indices))])

    return output

    





