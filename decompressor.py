import argparse
import zstandard as zstd
import os

from datetime import date, datetime
from fnmatch import fnmatch
from pathlib import Path

# Create an array and store all discovered credentials
# Used at the final export stage
credentials = []
pattern = "*.zst"

def main(args):

    start = datetime.now()

    print("=========================================================")
    print("Starting processing at: {}".format(start))
    print("Searching for the keywords: %s" % args.keyword)
    print("=========================================================")

    for path, _, files in os.walk(Path(args.directory)):
        for name in files:
            if fnmatch(name, pattern):
                filepath = os.path.join(path, name)
                print("\nProcessing file: " + filepath)
                decompress(filepath, args.keyword, args.verbose)

    output(args.output)
    end = datetime.now()
    print('Processed in: {}'.format(end - start))

def decompress(path, keywords, verbose):    
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

                    for keyword in keywords:
                        if(keyword in line):
                            credentials.append(line)
                            
                            if(verbose):
                                print("Discovered: " + line)

                previous_line = lines[-1]
    #print("\n")

def output(extension):
    global credentials
    output_file = str(date.today()) + "-results" + extension

    with open(output_file, "w+", encoding="utf-8") as file:
        for credential in credentials:
            file.write('%s\n' % credential)

    print("=========================================================")
    print("Found a total of: %d findings." % len(credentials))
    print("Results have been generated at: " + output_file)
    print("=========================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Directory to enumerate .zst files", required=True)
    parser.add_argument("-k", "--keyword", help="Keyword(s) to search", required=True, type=str, nargs="+")
    parser.add_argument("-o", "--output", help="Output the results into a file.", type=str, choices=[".txt", ".csv"], default=".txt")
    parser.add_argument("-v", "--verbose", help="Enable verbosity", action="store_true")
    args = parser.parse_args()

    main(args)