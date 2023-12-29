import os
import pandas as pd
import traceback
import src.utils as utils
from importlib import reload

split_chroms_dir_path = 'split_vcf_chromosomes_csvs_compressed'
split_chroms_dir = os.listdir(split_chroms_dir_path)

for file in split_chroms_dir:
    utils.extract_tarball(os.path.join(split_chroms_dir_path, file))
