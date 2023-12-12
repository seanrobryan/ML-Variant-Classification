import re
import os
from importlib import reload
import src.utils as utils
import shutil

reload(utils)
# Get all files open in VCF_Extractor.py split between written and read
written_files_list = utils.find_all_file_writes('VCF_Extractor.py')
read_files_list = utils.find_all_file_reads('VCF_Extractor.py')


intersection = utils.intersection(written_files_list, read_files_list)
with open('intermediate_files.txt', 'w') as f:
    f.write('\n'.join(intersection))
    

with open('written_files_list.txt', 'w') as f:
    dif = utils.difference(written_files_list, intersection, sort=False)
    f.write('\n'.join(dif))

with open('read_files.txt', 'w') as f:
    dif = utils.difference(read_files_list, intersection, sort=False)
    f.write('\n'.join(dif))


# Get contents of current intermediates and outputs directory
intermediates_and_output_dir = 'intermediates_and_outputs'
intermediate_and_output_dir_contents = os.listdir(intermediates_and_output_dir)

# Identify which files are in common between existing intermediates and outputs directory
#   the files identified as being read in VCF_Extractor.py
intersection = utils.intersection(written_files_list, intermediate_and_output_dir_contents)
print('Written files length:', len(written_files_list))
print('Output directory length:', len(intermediate_and_output_dir_contents))

# Intersection length != written files length != output directory length => still don't have all the files sorted correctly
print('Intersection length:', len(intersection)) 

# Find the differences
diff = utils.difference(written_files_list, intermediate_and_output_dir_contents, 'both')
print('Differences:', '\nIn written files:', diff['left'], '\nIn output directory:', diff['right'])

print('In written files list')
for f in diff['left']:
    print(utils.find_file(root_dir='.', file_name=f, filter_dirs=utils.remove_hidden, topdown=True))
    
print('Currently in intermediates and output dir')
for f in diff['right']:
    print(utils.find_file(root_dir='.', file_name=f, filter_dirs=utils.remove_hidden, topdown=True))
    
# Identify intermediates as the intersection between files written to and files read from
print('Identifying intermediates...')
in_input_and_output =  utils.intersection(written_files_list, read_files_list)
print(in_input_and_output)

# Moving intermediates to an intermediate directory
print('Moving overlapping files to intermediates directory')
intermediates_dir = 'intermediates'
os.mkdir(intermediates_dir)
for file in in_input_and_output:
    shutil.move(os.path.join(intermediates_and_output_dir, file), os.path.join(intermediates_dir, file))

# Renaming old intermediates and output directory to just outputs
os.rename(intermediates_and_output_dir, 'outputs')

reload(utils)
# Files that are read from but not written to are inputs
input_files_list = utils.difference(read_files_list, written_files_list, return_side='left')
print('Input files:', len(input_files_list), 'files\n', input_files_list)

# Find inputs files and move them to the inputs directory if not already there
for file in input_files_list:
    found_file = utils.find_file('.', file_name=file, filter_dirs=utils.remove_hidden, topdown=True)
    if len(found_file) == 0:
        print(file, 'could not be located')
        continue
    elif len(found_file) == 1:
        found_file = found_file[0]
    else:
        print(f"Multiple versions of {file} found. Please manually check")
    
    if os.path.dirname(found_file) == './inputs':
        print(f"{file} is already in ./inputs")
    else:
        print(f"Moving {file} to ./inputs")
        shutil.move(file, os.path.join('inputs', os.path.basename(file)))


# Identifying how many input files are missing
input_dir_contents = os.listdir('./inputs')
print(f"Current input directory contents: {len(input_dir_contents)} files\n", input_dir_contents)

input_file_differences = utils.difference(input_files_list, input_dir_contents, 'both')
print('Input file differences:', '\nIn input files:', diff['left'], '\nIn input files directory:', diff['right'])

# How many of these can be found in the zips?
zips_dir = './zips'
zips_dir_content = os.listdir(zips_dir)
print(f"Zips directory content: {len(zips_dir_content)}\n", zips_dir_content)

zipped_file_basenames = [os.path.splitext(os.path.splitext(os.path.basename(f))[0])[0] for f in zips_dir_content]
input_file_basenames = [os.path.splitext(f)[0] for f in input_files_list]

zip_input_interesection = utils.intersection(zipped_file_basenames, input_file_basenames)
print('Files in zip directory also in input files list:\n', zip_input_interesection)

