
import re

male_pronouns = [
    "he",
    "him"
]

male_words = [
    'human', 'person', 'man', 'boy', 'gentleman'
]

female_pronouns = [
    "she",
    "her"
]    

female_words = [
    'human', 'person', 'woman', 'girl', 'lady'
]

many_pronouns = [
    "they", "them"
]

many_words = [
    'human', 'person', 'men', 'boys', 'gentlemen', 'women', 'girls', 'ladies'
]

object_pronouns = [
    "it"
]

def split_sentence(sentence):
    sentence = re.sub(r'([.,?!])', r' \1', sentence)
    words = sentence.split()
    return words

def reference_replacer(word, sentence):
    sentence_words = split_sentence(sentence)

    replaced_sentence = []
    for sw in sentence_words:
        if sw in male_pronouns:
            for m in male_words:
                if m in word:
                    replaced_sentence.append(word)

        elif sw in female_pronouns:
            for f in female_words:
                if f in word:
                    replaced_sentence.append(word)
        
        elif sw in many_pronouns:
            for m in many_words:
                if m in word:
                    replaced_sentence.append(word)

        elif sw in object_pronouns:
            replaced_sentence.append(word)

        else:
            replaced_sentence.append(sw)

    return ' '.join(replaced_sentence)



print(reference_replacer("a red hat", "what shape is it?"))
            
