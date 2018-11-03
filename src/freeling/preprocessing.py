from hunspell import Hunspell
from unidecode import unidecode
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.metrics.distance import edit_distance
import string
import zipfile
import re
from langdetect import detect
from functools import reduce
    
hunsp = Hunspell('Spanish')
table = str.maketrans('', '', string.punctuation)

def is_not_spanish_line(line):
    try:
        return detect(line) != 'es'
    except:
        return True

def correct_hyphen(lines):
    for line_index, line in enumerate(lines):
        if line != []:
            last_word = line[-1].strip()
            last_char = last_word[-1]
            if last_char == '-' and  line_index+1 < len(lines):
                next_line = lines[line_index+1]
                if len(next_line) > 0:
                    first_word_next_line = next_line[0]
                    first_word_clean_next_line = first_word_next_line.translate(table)
                    if hunsp.spell(last_word[:-1]+first_word_clean_next_line):
                        lines[line_index+1].pop(0)
                        new_line = line[:-1]
                        new_line.append(last_word[:-1]+first_word_next_line)
                        lines[line_index] = new_line
                        if lines[line_index+1] == []:
                            lines.pop(line_index+1) 

def has_too_many_errors(sentence):
    clean_words = [word.translate(table) for word in sentence]
    words_suggest = [(word, list(hunsp.suggest(word))[:3]) for word in clean_words if not hunsp.spell(word)]
    levenshtein_errors = []
    for duple in words_suggest:
        levenshtein_errors.append(reduce(lambda x, y: x + edit_distance(y, duple[0]), duple[1], 0) / len(duple[1]))
    avg_levenshtein_errors = reduce(lambda x, y: x + y, levenshtein_errors, 0) / len(levenshtein_errors) if levenshtein_errors != [] else 0
    return len(words_suggest) > 0.6 * len(clean_words) and avg_levenshtein_errors >= 1.5

def has_too_many_symbols(sentence):
    return len(re.findall(r'[^A-Za-z0-9\s]', unidecode(sentence))) * 100 / len(sentence) > 15

def calculate_avg_line_length(lines):
    (count_non_empty_lines, sum_non_emtpy_lines_length) = reduce(lambda x, y: (x[0] + 1, x[1] + len(y.strip())) if len(y.strip()) > 0 else x, lines, (0, 0))
    if count_non_empty_lines > 0:
        return sum_non_emtpy_lines_length / count_non_empty_lines 
    else:
        return 0
    

def eliminate_rubish_lines(lines, avg_line_length):
    line_idxs_remove = []
    possible_rubish_zone = True
    for line_index, line in enumerate(lines):
        line = line.strip()
        if line == '':
            possible_rubish_zone = True
        elif has_too_many_symbols(line):
            possible_rubish_zone = True
            line_idxs_remove.append(line_index)
        elif possible_rubish_zone and len(line) < avg_line_length:
            line_idxs_remove.append(line_index)
        else:
            possible_rubish_zone = False
    for idx_remove in reversed(line_idxs_remove):
        lines[idx_remove] = '\n'
     
def lines_to_raw(lines):
    raw = ''
    for line in lines:
        raw += ' '.join(line) 
        raw += '\n'
    return raw

def discard_sentence_with_errors(sentences):
    sentence_idx_discard = []
    for sentence_index, sentence in enumerate(sentences):
        if is_not_spanish_line(sentence) or has_too_many_errors(sentence):
            sentence_idx_discard.append(sentence_index)
    for idx_discard in reversed(sentence_idx_discard):
        sentences.pop(idx_discard)
             

def read_zip_file(filepath):
    with zipfile.ZipFile(filepath, 'r') as zfile:
        for zip_info in zfile.infolist():
            yield (zip_info.filename, zfile.open(zip_info).read().decode('utf-8'))

def preprocess(zip_file_path):
    for filename, content in read_zip_file(zip_file_path):
        result_path = '/home/pablo/proygrado/freeling/share/freeling/APIs/python3/diarios_corregidos/' + filename
        lines = content.split('\n')
        avg_line_length = calculate_avg_line_length(lines)
        eliminate_rubish_lines(lines, avg_line_length) 
        lines_split_in_words = [line.split() for line in lines]
        correct_hyphen(lines_split_in_words)
        raw_text = lines_to_raw(lines_split_in_words)
        raw_text = re.sub(r'\n\n+', '.\n', raw_text)
        raw_text = re.sub(r'\.\.\n', '.\n', raw_text)
        sentences = sent_tokenize(raw_text)
        discard_sentence_with_errors(sentences)
        result_file = open(result_path,'w')
        result_file.write('\n'.join(sentences))
        result_file.close()

preprocess('/home/pablo/proygrado/freeling/share/freeling/APIs/python3/diarios.zip')
