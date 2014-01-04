cd .

# python utils/import-flat-files.py st 0 80000
# python utils/import-flat-files.py pe 0 80000
# python utils/import-flat-files.py se 0 1000
# python utils/import-flat-files.py cb 0 70
# python utils/import-flat-files.py sb 0 70

echo "Importing Stops"
python utils/import-flat-files.py st 0 999999
python utils/import-flat-files.py st 1000000 1000000
python utils/import-flat-files.py st 2000000 1000000
python utils/import-flat-files.py st 3000000 1000000
python utils/import-flat-files.py st 4000000 1000000
python utils/import-flat-files.py st 5000000 1000000
python utils/import-flat-files.py st 6000000 1000000
python utils/import-flat-files.py st 7000000 1000000
python utils/import-flat-files.py st 8000000 1000000
python utils/import-flat-files.py st 9000000 1000000
python utils/import-flat-files.py st 10000000 1000000
python utils/import-flat-files.py st 11000000 1000000
python utils/import-flat-files.py st 12000000 1000000
python utils/import-flat-files.py st 13000000 1000000
python utils/import-flat-files.py st 14000000 1000000
python utils/import-flat-files.py st 15000000 1000000
python utils/import-flat-files.py st 16000000 1000000
echo "Search import complete"

echo "Importing Persons"
python utils/import-flat-files.py pe 0 1000000
python utils/import-flat-files.py pe 1000000 1000000
python utils/import-flat-files.py pe 2000000 1000000
python utils/import-flat-files.py pe 3000000 1000000
python utils/import-flat-files.py pe 4000000 1000000
python utils/import-flat-files.py pe 5000000 1000000
python utils/import-flat-files.py pe 6000000 1000000
python utils/import-flat-files.py pe 7000000 1000000
python utils/import-flat-files.py pe 8000000 1000000
python utils/import-flat-files.py pe 9000000 1000000
python utils/import-flat-files.py pe 10000000 1000000
python utils/import-flat-files.py pe 11000000 1000000
python utils/import-flat-files.py pe 12000000 1000000
python utils/import-flat-files.py pe 13000000 1000000
python utils/import-flat-files.py pe 14000000 1000000
python utils/import-flat-files.py pe 15000000 1000000
python utils/import-flat-files.py pe 16000000 1000000
python utils/import-flat-files.py pe 17000000 1000000
echo "Persons import complete"

echo "Importing Searches"
python utils/import-flat-files.py se 0 100000
python utils/import-flat-files.py se 100000 100000
python utils/import-flat-files.py se 200000 100000
python utils/import-flat-files.py se 300000 100000
python utils/import-flat-files.py se 400000 100000
python utils/import-flat-files.py se 500000 100000
echo "Search import complete"

echo "Importing Contraband"
python utils/import-flat-files.py cb 0 50000
python utils/import-flat-files.py cb 50000 50000
python utils/import-flat-files.py cb 100000 50000
echo "Contraband import complete"

echo "Importing SearchBasis"
python utils/import-flat-files.py sb 0 100000
python utils/import-flat-files.py sb 100000 100000
python utils/import-flat-files.py sb 200000 100000
python utils/import-flat-files.py sb 300000 100000
python utils/import-flat-files.py sb 400000 100000
python utils/import-flat-files.py sb 500000 100000
python utils/import-flat-files.py sb 600000 100000
echo "SearchBasis import complete"
