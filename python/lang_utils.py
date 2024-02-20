"""
Language Utilities
@author     Teki Chan
@since      30 Jan 2024
"""
import nltk
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize
import os
import re
from pypdf import PdfReader
from string import printable

def get_text_tokens(pdf_reader):
    """
    Get a list of text tokens, aka sentences, from PDF Reader
    """
    text_tokens = list()
    for page in pdf_reader.pages:
        text = page.extract_text()
        new_text = re.sub(r'\s+', ' ', text)    # Replace successive whitespaces into single
        new_text = re.sub("[^{}]+".format(printable), "", new_text) # Remove invisible chars
        nltk_tokens = nltk.sent_tokenize(new_text)
        text_tokens.extend(nltk_tokens)
    return text_tokens

def is_balanced(sentence, open_bracket='(', close_bracket=')'):
    """
    Whether the sentence has balanced brackets
    """
    return sentence.count(open_bracket) == sentence.count(close_bracket)

def massage_tokens(text_tokens):
    """
    Massage given list of text tokens
    """
    new_text_tokens = list()
    idx = 0
    while idx < len(text_tokens):
        current_text = text_tokens[idx].strip()
        if not current_text:
            # skip empty line
            pass
        elif idx > 0 and not re.match('\w', current_text[0]):
            # merge previous if not starting with word
            new_text_tokens[-1] = new_text_tokens[-1] + ' ' + current_text
        elif idx > 0 and not is_balanced(new_text_tokens[-1]) and not is_balanced(current_text):
            # merged previous if brackets not balanced
            new_text_tokens[-1] = new_text_tokens[-1] + ' ' + current_text
        elif idx > 0 and re.match('^\d+\s*\.$', new_text_tokens[-1]):
             # previous numbered points
             new_text_tokens[-1] = new_text_tokens[-1] + ' ' + current_text
        elif re.search(':\s*\d+\s*\.', current_text):
            # numbered point before colon
            searched = re.search(':\s*\d+\s*\.', current_text)
            new_text_tokens.append(current_text[:searched.start() + 1].strip())
            new_text_tokens.append(current_text[searched.start() + 1:].strip())
        else:
            new_text_tokens.append(current_text)
        idx += 1
    return new_text_tokens

def get_path_tokens(pdf_path_list):
    """
    Process each file from the list and save the result in the dict
    """
    path_tokens_dict = dict()
    for pdf_path in pdf_path_list:
        reader = PdfReader(pdf_path)
        text_tokens = get_text_tokens(reader)
        new_text_tokens = massage_tokens(text_tokens)
        file_name = os.path.basename(pdf_path)
        path_tokens_dict[file_name] = new_text_tokens
    return path_tokens_dict

def is_citation(text_pair_line):
    """
    Whether the given sentence is citation
    """
    text_line = text_pair_line[1]
    searched_p1 = re.search('[\w\.,]+\s*\(\d{4}\)', text_line)
    searched_p2 = re.search('\([\w\.\s]+.*\d{4}\)', text_line)
    return True if searched_p1 or searched_p2 else False

def has_names(text_line, names):
    """
    Whether the given sentence has the given list of names
    """
    name_list = names.split(',')
    for name in name_list:
        if re.search(name, text_line, re.IGNORECASE):
            return True
    return False

def filter_citation(text_pair_list, authors=None):
    """
    Filter citation
    """
    filtered_pair = filter(is_citation, text_pair_list)
    if authors:
        filtered_pair = filter(lambda line_pair: has_names(line_pair[1], authors), filtered_pair)
    return filtered_pair

def split_digits(word_tokens):
    new_word_list = list()
    for word in word_tokens:
        new_word_list.extend(re.split('(\d+)',word))
    return new_word_list

def merge_hyphen_words(word_tokens):
    idx = 0
    new_word_list = list()
    while idx < len(word_tokens):
        current_word = word_tokens[idx]
        while idx + 1 < len(word_tokens) and \
            (current_word.endswith('-') or word_tokens[idx+1].startswith('-')):
            current_word = current_word + word_tokens[idx+1]
            idx += 1
        new_word_list.append(current_word)
        idx += 1
    return new_word_list

def get_file_tokens(text_pair_list, exclude_list):
    file_tokens_dict = dict()
    for text_pair in text_pair_list:
        filename = text_pair[0]
        sentence = text_pair[1]
        all_word_tokens = file_tokens_dict.get(filename, list())
        word_list = split_digits(word_tokenize(sentence))
        word_list = merge_hyphen_words(word_list)
        all_word_tokens.extend([word.lower() for word in word_list if re.search('[a-z]{2,}', word.lower()) and word.lower() not in exclude_list ])
        file_tokens_dict[filename] = all_word_tokens
    return file_tokens_dict

def _syllables(word):
    """
    preliminary method to count syllables
    """
    # Ref: https://stackoverflow.com/questions/14541303/count-the-number-of-syllables-in-a-word
    count = 0
    vowels = 'aeiouy'
    word = word.lower()
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count += 1
    if count == 0:
        count += 1
    return count 

def count_syllables(word, dict_dict=cmudict.dict(), option=0):
    try:
        syllable_counts = [len(list(y for y in x if y[-1].isdigit())) for x in dict_dict[word.lower()]]
        if len(syllable_counts) > 0:
            return syllable_counts[option]
        else:
            return 0
    except KeyError:
        return _syllables(word)
