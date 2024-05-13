# Initialize an empty CSV file
echo "url" > top_notebooks.csv

# Fetch kernels in batches until you have 100 or more
offset=0
while [ $(wc -l < top_notebooks.csv) -lt 100 ]; do
    kaggle kernels list --sort-by hotness --csv --page $((offset+1)) > temp.csv
    tail -n +2 temp.csv >> top_notebooks.csv
    offset=$((offset+1))
done

# Remove temporary file
rm temp.csv
