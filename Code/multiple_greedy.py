from collections import Counter
import random
import numpy as np

def score_kmer(kmer, background):
 
  score = 0
  for nucleotide in kmer:
    score += np.log2( (1 / background[nucleotide]) )  # Log-likelihood score
  return score

def find_greedy_motifs(sequences, k, num_motifs):
  
  motifs = []
  remaining_sequences = sequences.copy()

  for _ in range(num_motifs):
    print(_)
    # Find the motif in the remaining sequences
    motif, score = find_greedy_motif_single_randomized(remaining_sequences, k)
    motifs.append((motif, score))

    # Remove sequences containing the motif from remaining sequences
    remaining_sequences = [seq for seq in remaining_sequences if motif not in seq]

    # If no sequences remain for further motif discovery, terminate
    if not remaining_sequences:
      break

  return motifs

def find_greedy_motif_single_randomized(sequences, k, max_iterations=100):
 
  # Randomly initialize a motif
  motif = ''.join(random.choice('ACGT') for _ in range(k))

  best_motif = motif
  best_score = float('-inf')

  for _ in range(max_iterations):
    print(_)
    motif_scores = {}
    for sequence in sequences:
      for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i+k]
        motif_scores[kmer] = score_kmer(kmer, calculate_background(sequences))

    # Find the highest scoring k-mer (excluding the current motif)
    best_kmer, score = max(motif_scores.items(), key=lambda item: item[1])
    if score > best_score and best_kmer != motif:
      best_motif = best_kmer
      best_score = score

    # Randomly replace a position in the motif with the highest scoring k-mer
    replace_index = random.randint(0, k-1)
    motif = motif[:replace_index] + best_kmer[replace_index] + motif[replace_index+1:]

  return best_motif, best_score

def calculate_background(sequences):
 
  background = Counter()
  for sequence in sequences:

    background.update(sequence)

  total_count = sum(background.values())
  return {nucleotide: count / total_count for nucleotide, count in background.items()}


