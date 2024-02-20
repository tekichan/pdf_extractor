# How to use the program

There are two versions of the program. One is Python and one is Java. Please go to the corresponding section of your chosen language.

# Python

1. Install Python
2. Install dependency 

```bash
pip install -r requirements.txt
```

3. Install nltk popular data

```bash
python -m nltk.downloader popular
```

4. Run the program

- See help page

```bash
python pdf_extractor.py -h
```

- Run all stages for PDF files in `./pdf_dir/`

```bash
python pdf_extractor.py all -p ./pdf_dir
```

- Run extraction of PDF files in `./pdf_dir/` and save in `default_extracted.txt`

```bash
python pdf_extractor.py extract -p ./pdf_dir -e default_extracted.txt
```

- Run filtering of the extracted file `default_extracted.txt` for the author name `some_name` and save in `default_filtered.txt`

```bash
python pdf_extractor.py filter -e default_extracted.txt -f default_filtered.txt -a some_name
```

- Run word count of the filtered file `default_filtered.txt`, excluding words in `default_exclude.txt` and save in `default_output.xlsx`

```bash
python pdf_extractor.py count -f default_filtered.txt -x default_exclude.txt -o default_output.xlsx
```

- Run analysis of the output file `default_output.xlsx` to target pairs of words with higher than 0.5 correlation and save in `default_analysis.xlsx`

```bash
python pdf_extractor.py analyse -o default_output.xlsx -c 0.5 -l default_analysis.xlsx
```

# Java

TBC
