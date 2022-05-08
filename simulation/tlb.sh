#cpuid | grep -i tlb
cpuid -1 | grep -i tlb | awk 'ORS="\n"'  > file.csv
cp file.csv output.csv | awk 'BEGIN { FS = ":"; OFS = " " }'
#(echo "" ; cat file.txt) | sed 's/<newline>/<comma>/g' > output.csv
