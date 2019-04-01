## zstd-decompressor

Zstandard, or zstd as short version, is a fast lossless compression algorithm created by Facebook, targeting real-time compression scenarios at zlib-level and better compression ratios. source: [GitHub](https://github.com/facebook/zstd)

zstd-decompressor is a simple script I created to parse all .zst files in a directory (and all its subdirectories).

This script generates two .txt files
- {date}-results.txt: A file with all the discovered keywords.

**Requirements**
python3
zstandard library (pip3 install zstandard)

**Usage**
```
python decompressor.py -h
usage: decompressor.py [-h] -d DIRECTORY -k KEYWORD [-o {.txt,csv}]

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory to enumerate .zst files
  -k KEYWORD, --keyword KEYWORD
                        Keyword to search
  -o {.txt,csv}, --output {.txt,csv}
                        Output the results into a file.
```

**Example**
Example of using the script on a compressed, cleansed version of Collection #1 (35.31GB)
```
python decompressor.py -d "E:\ftp\Collection #1" -k "@baegmon.com"

. . .

Processing file: E:\ftp\Collection #1\USER PASS combos\98.txt.zst
Processing file: E:\ftp\Collection #1\USER PASS combos\99.txt.zst

Results have been generated at: 2019-04-01-results.txt
Processed in: 0:25:01.969913
```

**TODO**
- [ ] Implement exporting to .JSON
- [ ] Implement exporting to .CSV
