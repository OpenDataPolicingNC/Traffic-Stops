"""
Convert raw data into CSV files

Usage: python create-schema.py
"""
#!/usr/bin/env python
import os
import subprocess

RAW_DATA_DIR = '../raw-data'
CSV_DIR = os.path.join(RAW_DATA_DIR, 'csv')

mapping = {'length': (36, 44),
           'name': (59, 86)}

def create_schema(format_path, schema_path):
    """Create in2csv compatible schema file"""
    schema = ['column,start,length']
    with open(format_path, 'r') as f:
        version = f.readline().strip()
        num_columns = int(f.readline())
        start = 0
        for line in f:
            name = line[mapping['name'][0]:mapping['name'][1]].strip()
            length = int(line[mapping['length'][0]:mapping['length'][1]].strip())
            print name, start, length
            schema.append("%s,%s,%s" % (name, start, length))
            start += length
    with open(schema_path, 'w') as f:
        for line in schema:
            f.write("%s\n" % line)

def main():
    """Find all _format.txt files and convert their data files to CSV"""
    if not os.path.exists(RAW_DATA_DIR):
        print "First unpack raw data into ../raw-data"
        exit()
    files = filter(lambda x: x.endswith('format.txt'),
                   os.listdir(RAW_DATA_DIR))
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)
    for file_name in files:
        name, _ = file_name.split('_')
        format_path = os.path.join(RAW_DATA_DIR, file_name)
        data_path = os.path.join(RAW_DATA_DIR, name + '.txt')
        schema_path = os.path.join(CSV_DIR, name + '_schema.csv')
        csv_path = os.path.join(CSV_DIR, name + '.csv')
        create_schema(format_path, schema_path)
        print "in2csv -f fixed -s %s %s > %s" % (schema_path, data_path, csv_path)
        subprocess.call("in2csv -f fixed -s %s %s > %s" % (schema_path, data_path, csv_path), shell=True)

if __name__ == "__main__":
    main()
