import os
import gzip
import re
import tarfile
import urllib.parse

##### Functions for working with compressed files #####
def compress(input_file, output_file):
    try:
        with open(input_file, 'rb') as original_file, gzip.open(output_file, 'wb') as compressed_file:
            compressed_file.writelines(original_file)

        print(f"Compression complete. Compressed content saved to '{output_file}'")
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def decompress(input_file, output_file):
    try:
        with gzip.open(input_file, 'rb') as compressed_file, open(output_file, 'wb') as decompressed_file:
            # Read and decompress the content in chunks
            while True:
                chunk = compressed_file.read(1024)  # Adjust the chunk size as needed
                if not chunk:
                    break
                decompressed_file.write(chunk)
        
        print(f"Decompression complete. Decompressed content saved to '{output_file}'")
    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    return output_file
#######################################################

##### Functions for working with tarballs #####
def archive_files(input_files, output_archive):
    try:
        with tarfile.open(output_archive, 'w') as archive:
            if isinstance(input_files, str):
                archive.add(input_files)
            else:
                for file in input_files:
                    archive.add(file)
        print(f"Archiving complete. Files archived to '{output_archive}'")
    except FileNotFoundError:
        print("One or more input files not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def extract_tarball(tarball_file, keep_tar_file = False):
    file_path, file_name = os.path.dirname(tarball_file), os.path.basename(tarball_file)
    base_file_name = file_name.split('.')[0]
    tar_file = os.path.join(file_path, base_file_name + '.tar')
    archive_file = decompress(tarball_file, tar_file)
    try:
        with tarfile.open(archive_file, 'r') as archive:
            # archive.extractall(output_directory)
            archive.extractall()
        print("Unarchiving complete")
    except FileNotFoundError:
        print(f"Archive file '{archive_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    if not keep_tar_file:
        os.remove(tar_file)
        print(f"Removed archive file {tar_file}")

def compress_directory_contents_to_tarballs(directory, decompress_to, remove_dir = True):
    # Check if directory containing tarballs exists
    print(os.path.isdir(directory))
    if not os.path.isdir(directory):
        raise OSError(f"Directory {directory} not found.")
    # Check if output directory exists and whether it was empty prior to tarball extraction
    if not os.path.isdir(decompress_to):
        os.makedirs(decompress_to)
    else:
        warnings.warn(f"Output directory {decompress_to} already exists.")
        if len(os.listdir(decompress_to)) != 0:
            dir_contents = '\n'.join(os.listdir(decompress_dir_contents))
            warnings.warn(f"Output directory {decompress_to} was not empty. Pre-existing files are {dir_contents}")
    
    for file in os.listdir(directory):
        file = os.path.join(directory, file)

        # Archive file
        archived_file = os.path.join(decompress_to, os.path.splitext(os.path.basename(file))[0] + '.tar')
        archive_files(file, archived_file)

        # Compress archive
        compressed_archive = archived_file + '.gz'
        compress(archived_file, compressed_archive)

        os.remove(file)
        os.remove(archived_file)

    if remove_dir:
        os.removedirs(directory)
##############################################

##### Functions for comparing lists #####
def intersection(list1, list2, sort=True):
    # Convert both lists to sets and find the intersection
    intersection_ = list(set(list1) & set(list2))
    if sort: intersection_ = sorted(intersection_)
    return intersection_


def difference(list1, list2, return_side='l', sort=True):
    if return_side == 'l' or return_side == 'left':
        diff = list(set(list1) - set(list2))
    elif return_side == 'r' or return_side == 'right':
        diff = list(set(list2) - set(list1))
    elif return_side == 'b' or return_side == 'both':
        diff = {'left': list(set(list1) - set(list2)), 'right':list(set(list2) - set(list1))}
    else:
        raise ValueError(f"Unexpected value for return_side. Got {return_side} expected one of l, r, b, left, right, both")
    
    if sort:
        if isinstance(diff, list):
            diff = sorted(diff)
        else:
            diff['left'], diff['right'] = sorted(diff['left']), sorted(diff['right'])

    return diff
#########################################

##### Functions for searching directories ####
def enhanced_walk(root_dir, filter_dirs=None, filter_files=None, **kwargs):
    """
    A wrapper function for os.walk that applies filtering to directories and files.

    :param root_dir: The root directory to start the walk from.
    :param filter_dirs: A function to filter the directories. It takes a list of directories and returns a filtered list.
    :param filter_files: A function to filter the files. It takes a list of files and returns a filtered list.
    :param **kwargs: Additional keyword arguments to be passed to os.walk.
    :return: A generator that yields the same values as os.walk but with filtered directories and files.
    """
    for root, dirs, files in os.walk(root_dir, **kwargs):
        if filter_dirs is not None:
            dirs[:] = filter_dirs(dirs)
        
        if filter_files is not None:
            files = filter_files(files)

        yield root, dirs, files

def remove_hidden(dir_list):
    return [d for d in dir_list if d[0] != '.']


def find_file(root_dir, file_name, **kwargs):
    found_files = []
    for root, dirs, files in enhanced_walk(root_dir, **kwargs):
        if file_name in files:
            found_files.append(os.path.join(root, file_name))
    return found_files
##############################################

##### Functions for identifying read/write operations in a python file #####
def find_all_file_writes(file, inorder=True):
    validate_py_file(file)
    with open(file, 'r') as py_file:
        python_code = py_file.read()

        # Regex to find instances of file opening for writing (w, a, w+, a+, etc.)
        write_file_regex = r"open\(['\"](.*?)['\"],\s*['\"](w|a|w\+|a\+|x)['\"]"
        to_csv_regex = r'(\w+\.to_csv)\b'
        to_csv_regex = r'\.to_csv\((["\'])(.*?)\1\)'

        
        # Searching for all instances of file writing
        write_file_instances = re.findall(write_file_regex, python_code)
        to_csv_instances = re.findall(to_csv_regex, python_code)
        
        all_write_instances = write_file_instances + to_csv_instances
        write_file_instances = all_write_instances

        # print(to_csv_instances)
        # print(write_file_instances)
        # print(all_write_instances)
        # Extracting just the file names (not full paths) and ensuring uniqueness
        print(to_csv_instances)
        written_files = set()
        for file_path, _ in write_file_instances:
            # print(file_path, _)
            file_name = file_path.split('/')[-1]  # Extracting the file name
            written_files.add(file_name)

        # Make the written files list and sort if inorder is False
        written_files_list = list(written_files)
        if not inorder: written_files_list = sorted(written_files_list)
        
        return written_files_list
        
        
def find_all_file_reads(file, inorder=True):
    validate_py_file(file)
    with open(file, 'r') as py_file:
        python_code = py_file.read()

        # Regex to find instances of file opening for reading ('r')
        read_file_regex = r"open\(['\"](.*?)['\"],\s*['\"]r['\"]"
        read_csv_method_regex = r"\.read_csv\(['\"](.*?)['\"]\)"

        # Searching for all instances of file reading
        read_file_instances = re.findall(read_file_regex, python_code)
        read_csv_instances = re.findall(read_csv_method_regex, python_code)
        
        all_reads = read_file_instances + read_csv_instances
        
        read_file_instances = all_reads
        
        # Extracting just the file names (not full paths) and ensuring uniqueness
        read_files = set()
        for file_path in read_file_instances:
            file_name = file_path.split('/')[-1]  # Extracting the file name
            read_files.add(file_name)

        # Make the read files list and sort if inorder is False
        read_files_list = list(read_files)
        if not inorder: read_files_list = sorted(list(read_files_list))
        
        return read_files_list


def validate_py_file(file):
    if file.split('.')[-1] != 'py':
        raise ValueError(f"{file} is not a python file. Aborting search...")
############################################################################

##### Function parsing files ####
def safe_decode(value):
    if isinstance(value, str):
        return urllib.parse.unquote(value)
    return value