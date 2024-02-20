"""
Statistics Utilities
@author     Teki Chan
@since      30 Jan 2024
"""
from nltk.probability import FreqDist
import pandas as pd
from itertools import combinations
import re

def create_dataframe(freq):
    df = pd.DataFrame.from_dict(freq).reset_index()
    df.columns = ['index', 'word', 'count']
    df.set_index('word', inplace=True)
    df = df.drop('index', axis=1)
    return df

def merge_dataframes(file_tokens_dict):
    file_df_dict = dict()
    for filename, tokens in file_tokens_dict.items():
        # Produce frequency distribution
        freq = FreqDist(tokens).most_common()
        file_df_dict[filename] = create_dataframe(freq)
    merged_df = pd.concat(file_df_dict.values(), axis=1)
    merged_df.columns = file_df_dict.keys()
    merged_df.fillna(0, inplace=True)
    merged_df.sort_index(inplace=True)
    return merged_df

def read_output(output_path):
    df = pd.read_excel(output_path)
    return df.set_index('word')

def analyse_pair(df, pdf_file_list, min_corr_rate, text_pair_list):
    # Find all word pairs which appear in at least one of files
    word_pair_set = set()
    for file_name in pdf_file_list:
        word_pair_set.update({comb for comb in combinations(df[df[file_name] > 0].index, r=2)})
    
    # Filter those 
    word_pair_list = list()
    for comb in word_pair_set:
        comb_re1 = comb[0] + '[\s,-]*' + comb[1]
        comb_re2 = comb[1] + '[\s,-]*' + comb[0]
        for text_pair in text_pair_list:
            if re.search(comb_re1, text_pair[1]) or \
                re.search(comb_re2, text_pair[1]):
                word_pair_list.append(comb)
                break

    # Build the result of analysis
    result_list = []
    for comb in word_pair_list:
        corr_rate = df[pdf_file_list].loc[comb[0]].corr(df[pdf_file_list].loc[comb[1]])
        if corr_rate >= min_corr_rate:
            row = {
                'word_1': comb[0]
                , 'word_2': comb[1]
                , 'correlation': corr_rate
            }
            comb_re1 = comb[0] + '[\s,-]*' + comb[1]
            comb_re2 = comb[1] + '[\s,-]*' + comb[0]
            file_occurrence_dict = dict()
            for text_pair in text_pair_list:
                file_name = text_pair[0]
                text = text_pair[1]
                ocr = len(re.findall(comb_re1, text)) + len(re.findall(comb_re2, text))
                file_occurrence_dict[file_name] = file_occurrence_dict.get(file_name, 0) + ocr
            row.update(file_occurrence_dict)
            result_list.append(row)
    return pd.DataFrame.from_records(result_list)

def write_excel_word_counts(df, output_path, word_counts_columns, file_list):
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name='word_counts', index=True, columns=word_counts_columns+file_list)

def write_excel_paired_analysis(df, output_path):
    with pd.ExcelWriter(output_path) as writer:
        df.to_excel(writer, sheet_name='pair_analysis', index=False)    