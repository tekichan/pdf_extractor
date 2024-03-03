"""
Argument Utilities
@author     Teki Chan
@since      30 Jan 2024
"""
import argparse

def create_parser(
        default_extract='default_extracted.txt'
        , default_filter='default_filtered.txt'
        , default_operator='or'
        , default_exclude='default_exclude.txt'
        , default_out='default_output.xlsx'
        , default_corrrate='0.5'
        , default_analysis='default_analysis.xlsx'
    ):
    """
    Create a parser of program arguments
    """
    parser = argparse.ArgumentParser(
                prog='PDF Extractor',
                description='Extract PDF content'
            )
    parser.add_argument('stage', choices=['all', 'extract', 'filter', 'count', 'analyse']) 
    parser.add_argument('-p', '--pdf') 
    parser.add_argument('-e', '--ext', default=default_extract)
    parser.add_argument('-a', '--authors', default=None)
    parser.add_argument('-f', '--filter', default=default_filter)
    parser.add_argument('-x', '--exclude', default=default_exclude)
    parser.add_argument('-c', '--corrrate', default=default_corrrate)
    parser.add_argument('-o', '--out', default=default_out)
    parser.add_argument('-l', '--analysis', default=default_analysis)
    parser.add_argument('-op', '--operator', default=default_operator, choices=['and', 'or'])
    return parser

def usage(parser):
    """
    Print out how to use this program
    """
    parser.print_help()