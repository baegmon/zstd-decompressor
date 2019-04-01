import argparse
import zstandard as zstd
import os

from datetime import date, datetime
from fnmatch import fnmatch
from io import TextIOWrapper

# Create an array and store all discovered credentials
# Used at the final export stage
credentials = []

def main(args):
    pattern = "*.zst"
    start = datetime.now()

    for path, _, files in os.walk(args.directory):
        for name in files:
            if fnmatch(name, pattern):
                filepath = os.path.join(path, name)
                print("Processing file: " + filepath)
                decompress(filepath, args.keyword)
    
    output(args.output)
    end = datetime.now()
    print('Processed in: {}'.format(end - start))

def decompress(path, keyword):
    
    with open(path, "rb") as compressed_file_data:
        dctx = zstd.ZstdDecompressor()

        with dctx.stream_reader(compressed_file_data) as reader:
            previous_line = ""
            while True:
                chunk = reader.read(16777216)
                if not chunk:
                    break
                string_data = chunk.decode(encoding='utf-8', errors='ignore')
                lines = string_data.split("\n")
                for i, line in enumerate(lines[:-1]):
                    if i == 0:
                        line = previous_line + line

                    if(keyword in line):
                        credentials.append(line)

                previous_line = lines[-1]

def output(extension):
    global credentials
    credentials_export = str(date.today()) + "-results" + extension

    with open(credentials_export, 'w+', encoding="utf-8") as file:
        for credential in credentials:
            file.write('%s\n' % credential)
    
    print("\n")
    print("Results have been generated at: " + credentials_export)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory to enumerate .zst files", required=True)
    parser.add_argument("-k", "--keyword", help="Keyword to search", required=True)
    parser.add_argument("-o", "--output", help="Output the results into a file.", type=str, choices=['.txt', 'csv'], default='.txt')
    args = parser.parse_args()

    main(args)
