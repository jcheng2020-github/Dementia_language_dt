#Author: Junfu Cheng
import nltk
from nltk import pos_tag, word_tokenize
from nltk.tree import Tree
from collections import Counter
import re

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def get_metrics(text):
    # Tokenize and POS tagging
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    
    # Count total words
    word_count = len(tokens)
    
    # Initialize counters
    determiner_noun_phrases = 0
    verb_phrases_with_noun_phrases = 0
    coordinate_phrases = 0
    subordinate_phrases = 0
    subjects = 0

    # Analyze POS tags
    for i, (word, tag) in enumerate(pos_tags):
        # Determiner noun phrases (DT + NN)
        if tag in ['DT'] and (i + 1 < len(pos_tags) and pos_tags[i + 1][1] in ['NN', 'NNS']):
            determiner_noun_phrases += 1

        # Verb phrases with noun phrases (VB + NN)
        if tag.startswith('VB') and (i + 1 < len(pos_tags) and pos_tags[i + 1][1] in ['NN', 'NNS']):
            verb_phrases_with_noun_phrases += 1

        # Coordinate phrases (CC)
        if tag == 'CC':
            coordinate_phrases += 1

        # Subjects (using a simple heuristic, typically they are nouns or pronouns)
        if tag in ['NN', 'NNS', 'PRP', 'PRP$', 'DT']:
            subjects += 1

    # Subordinate vs coordinate phrases ratio
    subordinate_phrases = len([word for word in tokens if word.lower() in ['although', 'because', 'since', 'unless', 'if']])
    subordinate_coordinate_ratio = subordinate_phrases / (coordinate_phrases + 1e-5)  # Adding small value to avoid division by zero

    # Average word length
    avg_word_length = sum(len(word) for word in tokens) / word_count if word_count > 0 else 0

    # Determiner noun phrase ratio
    determiner_noun_phrase_ratio = determiner_noun_phrases / (word_count + 1e-5)  # Adding small value to avoid division by zero
    
    # Verb phrase with noun phrase ratio
    vp_np_ratio = verb_phrases_with_noun_phrases / (word_count + 1e-5)

    # Coordinate phrases ratio
    coordinate_phrases_ratio = coordinate_phrases / (word_count + 1e-5)

    # Proportion of subjects
    proportion_subjects = subjects / (word_count + 1e-5)

    # Return computed metrics
    return {
        'determiner_noun_phrase_ratio': determiner_noun_phrase_ratio,
        'word_count': word_count,
        'vp_np_ratio': vp_np_ratio,
        'coordinate_phrases_ratio': coordinate_phrases_ratio,
        'subordinate_ratio': subordinate_coordinate_ratio,
        'avg_word_length': avg_word_length,
        'proportion_subjects': proportion_subjects,
    }

# Example usage
if __name__ == "__main__":
    text_input = """Although he was tired, he decided to go for a run. The dog chased a squirrel and the cat watched from the window."""
    metrics = get_metrics(text_input)
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")
