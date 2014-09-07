"""
Convert raw data into CSV files

Usage: python create-schema.py
       python create-schema.py count
"""
#!/usr/bin/env python
import os
import subprocess
import sys

RAW_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'nc'))
CSV_DIR = os.path.join(RAW_DATA_DIR, 'csv')

mapping = {'length': (36, 44),
           'name': (59, 86)}


def line_count(fname):
    """Count number of lines in specified file"""
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


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
            schema.append("%s,%s,%s" % (name, start, length))
            start += length
    with open(schema_path, 'w') as f:
        for line in schema:
            f.write("%s\n" % line)

def main():
    """Find all _format.txt files and convert their data files to CSV"""
    if not os.path.exists(RAW_DATA_DIR):
        print("First unpack raw data into ../raw-data")
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
        if len(sys.argv) > 1 and sys.argv[1] == 'count':
            data_count = line_count(data_path)
            csv_count = line_count(csv_path)
            print(name)
            print('DAT', data_count)
            print('CSV', csv_count)
            continue
        create_schema(format_path, schema_path)
        print("in2csv -e iso-8859-1 -f fixed -s {} {} > {}".format(schema_path, data_path, csv_path))
        subprocess.call("in2csv -e iso-8859-1 -f fixed -s {} {} > {}".format(schema_path, data_path, csv_path), shell=True)
        print(r"sed -i 's/\x0//g' {}".format(csv_path))
        subprocess.call(r"sed -i 's/\x0//g' {}".format(csv_path), shell=True)
        

if __name__ == "__main__":
    main()
