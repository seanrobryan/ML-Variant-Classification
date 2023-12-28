import re
from src.utils import decompress
import os

dvd_dir = '/Users/seanryan/Documents/School/Graduate/Variant_Classification_Braun/files_from_MORL_argon/DVD/9_1_1/final_output/'
morl_dvd_dir = '/home/srryn/hpchome/DVD/versions/9_1_1/final_outputs/'

active_dir = morl_dvd_dir

# Open file, this will read in the header
dvd_file = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes.vcf')
dvd_gz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes.vcf.gz')
dvd_bgz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes.vcf.bgz')

if not os.path.isfile(dvd_file):
    decompress(dvd_bgz, dvd_file)

def find_lines_starting_with_pattern(filename, pattern):
    line_numbers = []
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file):
            if re.match(pattern, line):
                line_numbers.append(line_number)
    return line_numbers

sum_of_lines = 0
header_lines = 289

chroms_names = ['MT', 'X'] + [str(x) for x in range(1,23)]

from typing import List
def find_lines_starting_with_chromosome(filename:str, chromosomes: List[str]):
    patterns = [rf'^{c}\t' for c in chromosomes]
    pattern_to_lines_dict = {p:list() for p in patterns}
    with open(filename, 'r') as file:
        for line_number, line in enumerate(file):
            for pattern, chromosome in zip(patterns, chromosomes):
                if re.match(pattern, line):
                    pattern_to_lines_dict[chromosome].append(tuple([line_number, line]))
            if line_number % 10000 == 0:
                print(line_number)
    return pattern_to_lines_dict


lines_by_chromosome = find_lines_starting_with_patterns(dvd_file, chroms_names)



for c in chroms_names:
    pattern = rf'^{c}\t'  # Regular expression pattern for lines starting with '10\t'
    print(pattern)
    print(c)
    line_numbers_matching_pattern = find_lines_starting_with_pattern(dvd_file, pattern)
    num_line_number_matches = len(line_numbers_matching_pattern)
    print(num_line_number_matches)
    sum_of_lines += num_line_number_matches

    try:
        print(pd.read_csv(f'chromosome_{c}_records.csv').shape)
    except Exception as e:
        print(f"CSV for {c} not created yet")

    if num_line_number_matches == 0:
            break

print(sum_of_lines)
# print("Line numbers that start with '10\\t':", line_numbers_matching_pattern)

print(len(line_numbers_matching_pattern))
with open(dvd_file, 'rt') as f:
    lines = f.readlines()
    print(lines[1900000])



print(line_numbers_matching_pattern[26296])
print(line_numbers_matching_pattern[26297])
print(line_numbers_matching_pattern[26298])

# 1910114