import unicodecsv

with open('../analysis_process_01/csv/test.csv', 'rb+') as f:
    reader = unicodecsv.DictReader(f)
    