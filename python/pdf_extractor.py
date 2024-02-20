"""
PDF Extractor Main Program
@author     Teki Chan
@since      30 Jan 2024
"""
import arg_utils
import file_utils
import lang_utils
import os
import stat_utils
import sys

if __name__ == '__main__':
    """
    Main program starts
    """
    parser = arg_utils.create_parser()
    args = parser.parse_args()

    if args.stage in ['all', 'extract']:
        # Execute Extraction stage
        if not os.path.exists(args.pdf):
            # Exit when the given path does not exist
            print('ERROR: The given path {p} does not exist.'.format(p=args.pdf))
            sys.exit(-1)
        
        pdf_path_list = file_utils.get_pdf_files(args.pdf)        
        pdf_tokens = lang_utils.get_path_tokens(pdf_path_list)

        # Save the dict into a text file
        file_utils.write_output_extract(pdf_tokens, args.ext)
        if args.stage == 'extract':
            print('Extracting text from {s} to {d} was complete.'.format(s=args.pdf, d=args.ext))
            sys.exit(0)
    
    if args.stage in ['all', 'filter']:
        # Execute Filter stage
        if not os.path.exists(args.ext):
            print('ERROR: the given file {f} does not exist'.format(f=args.ext))
            sys.exit(-1)
        
        text_pair_list = file_utils.read_text_file(args.ext)
        filtered_pair = lang_utils.filter_citation(text_pair_list, args.authors)

        # Save the pair into a text file
        file_utils.write_output_filter(filtered_pair, args.filter)
        if args.stage == 'filter':
            print('Filtering text from {s} to {d} was complete.'.format(s=args.ext, d=args.filter))
            sys.exit(0)
    
    if args.stage in ['all', 'count']:
        # Execute Count (Statistics) stage
        if not os.path.exists(args.filter):
            print('ERROR: the given file {f} does not exist'.format(f=args.filter))
            sys.exit(-1)
        
        text_pair_list = file_utils.read_text_file(args.filter)
        exclude_list = file_utils.get_exclude_list(args.exclude)
        file_tokens_dict = lang_utils.get_file_tokens(text_pair_list, exclude_list)
        result_df = stat_utils.merge_dataframes(file_tokens_dict)

        # Get file column list
        pdf_file_list = list(result_df.columns)
        
        # Count Syllables
        result_df['syllables'] = result_df.index.map(lang_utils.count_syllables)
        # Count non-zero columns
        result_df['file_count'] = (result_df[pdf_file_list] > 0).sum(axis=1)
        # Total occurrence
        result_df['occurrence'] = result_df[pdf_file_list].sum(axis=1)

        # Save the dataframe into an Excel file
        stat_utils.write_excel_word_counts(result_df, args.out, ['syllables', 'file_count', 'occurrence'], pdf_file_list)
        if args.stage == 'count':
            print('Statatics of {s} is saved in {d} completely.'.format(s=args.filter, d=args.out))
    
    if args.stage in ['all', 'analyse']:
        # Execute Pair Analysis stage
        if not os.path.exists(args.out):
            print('ERROR: the given file {f} does not exist'.format(f=args.out))
            sys.exit(-1)
        
        output_df = stat_utils.read_output(args.out)
        # Get file column list
        pdf_file_list = list(output_df.columns)
        # Read File of File-Text
        text_pair_list = file_utils.read_text_file(args.filter)
        # Pair analysis
        paired_df = stat_utils.analyse_pair(output_df, pdf_file_list, float(args.corrrate), text_pair_list)
        stat_utils.write_excel_paired_analysis(paired_df, args.analysis)
        if args.stage == 'analyse':
            print('Statatics of {s} is saved in {d} completely.'.format(s=args.out, d=args.analysis))
        else:
            # Final output message
            print('All processes done. Statatics of {s} is saved {o} and {d} completely.'.format(s=args.pdf, o=args.out, d=args.analysis))
    