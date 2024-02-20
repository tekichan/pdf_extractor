"""
File Utilities
@author     Teki Chan
@since      30 Jan 2024
"""
import json
import os

def filter_pdf_file(dir):
    """
    List all PDF files in the given directory
    """
    result = list()
    for root, dirs, files in os.walk(dir):
        for file in files:
            full_path = os.path.join(root, file)
            if os.path.isfile(full_path) and file.endswith('.pdf'):
                result.append(full_path)
    return result

def get_pdf_files(pdf_path):
    if os.path.isdir(pdf_path):
        # The given path is a directory
        return filter_pdf_file(pdf_path)
    else:
        # The given path is a single file
        return [ pdf_path ]

def write_output_extract(file_tokens_dict, output_path):
    """
    Write the result to an output file
    """
    with open(output_path, 'w') as fw:
        # Print header
        fw.write('\t'.join(['Filename', 'Sentence']))
        fw.write('\n')
        for file_name, text_list in file_tokens_dict.items():
            for line in text_list:
                fw.write('\t'.join([file_name, line]))
                fw.write('\n')  

def read_text_file(text_file):
    """
    Read the given text file and return a list of sentences
    """
    with open(text_file, 'r') as fr:
        fr.readline()
        text_list = [line.strip().split('\t') for line in fr.readlines()]
    return text_list

def write_output_filter(text_pair_list, output_path):
    """
    Write the result to an output file
    """
    with open(output_path, 'w') as fw:
        # Print header
        fw.write('\t'.join(['Filename', 'Sentence']))
        fw.write('\n')        
        for line_pair in text_pair_list:
            fw.write('\t'.join(line_pair))
            fw.write('\n')

def get_exclude_list(exclude_file):
    """
    Get List of excluded words from a gile
    """
    if exclude_file is None:
        return list()
    else:
        with open(exclude_file, 'r') as fr:
            exclude_list = [line.strip() for line in fr.readlines()]
        return exclude_list
    
def save_json(dict_obj, file_name):
    with open(file_name, 'w') as fw:
        json.dump(dict_obj, fw)

def read_json(file_name):
    with open(file_name, 'r') as fr:
        json_obj = json.load(fr)
    return json_obj