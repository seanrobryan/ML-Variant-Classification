import os
import pandas as pd
from importlib import reload
import src.utils as utils

morl_dvd_dir = '/home/srryn/hpchome/DVD/versions/9_1_1/final_outputs/'
active_dir = os.path.join(morl_dvd_dir, 'delete_later')

# Open file, this will read in the header
# dvd_file = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf')
'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf'
# dvd_file = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf')
# dvd_gz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes.vcf.gz')
# dvd_bgz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf.bgz')

# dvd_gz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_processed_to_ascii.vcf.gz')


dvd_gz = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_gunzip_ascii_bgzip.gz')
dvd_gz_index = os.path.join(active_dir, 'DVDv9_e_20220414.arr.posthoc_annotes_gunzip_ascii_bgzip.gz.tbi')

dvd_file = '/home/srryn/hpchome/DVD/versions/9_1_1/final_outputs/DVDv9_e_20220414.arr.posthoc_annotes.vcf'
def subset_vcf(input_file, output_file, n_lines):
    # Made a new txt (vcf) file from the first n_lines lines of the dvd vcf to look at it manually
    with open(input_file, 'r') as dvd:
        with open(output_file, 'w') as out_file:
            for i in range(0, n_lines):
                l = dvd.readline()
                # print(l)
                out_file.write(l)

subset_vcf(dvd_file, 'dvd_subset.txt', 7500)

# Preprocessing out duplicate columns (artifacts from lazy merging)
dfs = []
id_cols = ['CHROM', 'POS', 'REF', 'ALT']
dup_cols = [f"{base_col}_{alt}" for base_col in id_cols for alt in ['x', 'y']]
for f in os.scandir('chromosomes_w_ddg'):
    df = pd.read_csv(f.path, index_col=0, encoding='utf-8')
    df.drop(columns=dup_cols, inplace=True)
    dfs.append(df)

all_dfs = pd.concat(dfs)

value_counts_per_column = {}
for column in all_dfs.columns:
    value_counts_per_column[column] = all_dfs[column].value_counts()

value_counts_per_column

all_dfs.loc[:, all_dfs.count(axis=0) > all_dfs.shape[0]*0.75]

all_dfs.shape

all_dfs.count(axis=0) 

# all_dfs.loc[:, all_dfs.count(axis=0) > ]

import re

hgmd_string = """##INFO=<ID=HGMD_CONFIDENCE,Number=.,Type=String,Description="NA. Single variant with multiple record entries delimited by '|'.">
##INFO=<ID=HGMD_DISEASE,Number=.,Type=String,Description="NA. Single variant with multiple record entries delimited by '|'.">
##INFO=<ID=HGMD_HGVS,Number=.,Type=String,Description="NA. Single variant with multiple record entries delimited by '|'.">
##INFO=<ID=HGMD_OMIM_REF,Number=.,Type=String,Description="NA. Single variant with multiple record entries delimited by '|'.">
##INFO=<ID=HGMD_PMID,Number=.,Type=String,Description="NA. Single variant with multiple record entries delimited by '|'.">
##INFO=<ID=HGMD_RSID,Number=.,Type=String,Description="NA. Single variant with multiple record entries delimited by '|'.">
##INFO=<ID=HGMD_VARIANTTYPE,Number=.,Type=String,Description="NA. Single variant with multiple record entries delimited by '|'.">
##INFO=<ID=HGMD_MAX_MAF,Number=.,Type=Float,Description="Max MAF for HGMD, in range (0,1)">
##INFO=<ID=HGMD_MAX_MAF_SOURCE,Number=.,Type=String,Description="Max MAF population for HGMD"> """

pattern = r"<ID=HGMD_[\w]+,"
hgmd_cols = []
for match in re.findall(pattern, hgmd_string):
    hgmd_cols.append(match[4:-1])


gnomad_string = """##INFO=<ID=gnomad_AN,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN and gnomad_exome_AN">
##INFO=<ID=gnomad_filters,Number=.,Type=String,Description="vcf FILTER values as an INFO tag for annotation.">
##INFO=<ID=gnomad_AC_nfe_seu_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_nfe_seu and gnomad_exome_AC_nfe_seu">
##INFO=<ID=gnomad_AC_fin_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_fin_female and gnomad_exome_AC_fin_female">
##INFO=<ID=gnomad_AC_afr_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_afr_male and gnomad_exome_AC_afr_male">
##INFO=<ID=gnomad_AC_eas_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_eas_female and gnomad_exome_AC_eas_female">
##INFO=<ID=gnomad_AC_afr_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_afr_female and gnomad_exome_AC_afr_female">
##INFO=<ID=gnomad_AC_nfe_onf_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_nfe_onf and gnomad_exome_AC_nfe_onf">
##INFO=<ID=gnomad_AC_fin_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_fin_male and gnomad_exome_AC_fin_male">
##INFO=<ID=gnomad_AC_nfe_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_nfe_female and gnomad_exome_AC_nfe_female">
##INFO=<ID=gnomad_AC_asj_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_asj_male and gnomad_exome_AC_asj_male">
##INFO=<ID=gnomad_AC_oth_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_oth_female and gnomad_exome_AC_oth_female">
##INFO=<ID=gnomad_AC_nfe_nwe_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_nfe_nwe and gnomad_exome_AC_nfe_nwe">
##INFO=<ID=gnomad_AC_nfe_est_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_nfe_est and gnomad_exome_AC_nfe_est">
##INFO=<ID=gnomad_AC_eas_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_eas_male and gnomad_exome_AC_eas_male">
##INFO=<ID=gnomad_AC_nfe_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_nfe_male and gnomad_exome_AC_nfe_male">
##INFO=<ID=gnomad_AC_asj_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_asj_female and gnomad_exome_AC_asj_female">
##INFO=<ID=gnomad_AC_amr_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_amr_male and gnomad_exome_AC_amr_male">
##INFO=<ID=gnomad_AC_amr_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_amr_female and gnomad_exome_AC_amr_female">
##INFO=<ID=gnomad_AC_oth_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_oth_male and gnomad_exome_AC_oth_male">
##INFO=<ID=gnomad_AC_nfe_bgr_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AC_nfe_bgr">
##INFO=<ID=gnomad_AC_sas_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AC_sas_male">
##INFO=<ID=gnomad_AC_nfe_swe_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AC_nfe_swe">
##INFO=<ID=gnomad_AC_eas_jpn_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AC_eas_jpn">
##INFO=<ID=gnomad_AC_eas_kor_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AC_eas_kor">
##INFO=<ID=gnomad_AC_eas_oea_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AC_eas_oea">
##INFO=<ID=gnomad_AC_sas_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AC_sas_female">
##INFO=<ID=gnomad_AC_asj_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_asj and gnomad_exome_AC_asj">
##INFO=<ID=gnomad_AC_fin_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_fin and gnomad_exome_AC_fin">
##INFO=<ID=gnomad_AC_oth_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_oth and gnomad_exome_AC_oth">
##INFO=<ID=gnomad_AN_nfe_seu_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_nfe_seu and gnomad_exome_AN_nfe_seu">
##INFO=<ID=gnomad_AN_fin_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_fin_female and gnomad_exome_AN_fin_female">
##INFO=<ID=gnomad_AN_afr_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_afr_male and gnomad_exome_AN_afr_male">
##INFO=<ID=gnomad_AN_eas_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_eas_female and gnomad_exome_AN_eas_female">
##INFO=<ID=gnomad_AN_afr_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_afr_female and gnomad_exome_AN_afr_female">
##INFO=<ID=gnomad_AN_nfe_onf_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_nfe_onf and gnomad_exome_AN_nfe_onf">
##INFO=<ID=gnomad_AN_fin_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_fin_male and gnomad_exome_AN_fin_male">
##INFO=<ID=gnomad_AN_nfe_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_nfe_female and gnomad_exome_AN_nfe_female">
##INFO=<ID=gnomad_AN_asj_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_asj_male and gnomad_exome_AN_asj_male">
##INFO=<ID=gnomad_AN_oth_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_oth_female and gnomad_exome_AN_oth_female">
##INFO=<ID=gnomad_AN_nfe_nwe_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_nfe_nwe and gnomad_exome_AN_nfe_nwe">
##INFO=<ID=gnomad_AN_nfe_est_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_nfe_est and gnomad_exome_AN_nfe_est">
##INFO=<ID=gnomad_AN_eas_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_eas_male and gnomad_exome_AN_eas_male">
##INFO=<ID=gnomad_AN_nfe_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_nfe_male and gnomad_exome_AN_nfe_male">
##INFO=<ID=gnomad_AN_asj_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_asj_female and gnomad_exome_AN_asj_female">
##INFO=<ID=gnomad_AN_amr_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_amr_male and gnomad_exome_AN_amr_male">
##INFO=<ID=gnomad_AN_amr_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_amr_female and gnomad_exome_AN_amr_female">
##INFO=<ID=gnomad_AN_oth_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_oth_male and gnomad_exome_AN_oth_male">
##INFO=<ID=gnomad_AN_nfe_bgr_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AN_nfe_bgr">
##INFO=<ID=gnomad_AN_sas_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AN_sas_male">
##INFO=<ID=gnomad_AN_nfe_swe_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AN_nfe_swe">
##INFO=<ID=gnomad_AN_eas_jpn_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AN_eas_jpn">
##INFO=<ID=gnomad_AN_eas_kor_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AN_eas_kor">
##INFO=<ID=gnomad_AN_eas_oea_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AN_eas_oea">
##INFO=<ID=gnomad_AN_sas_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AN_sas_female">
##INFO=<ID=gnomad_AN_asj_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_asj and gnomad_exome_AN_asj">
##INFO=<ID=gnomad_AN_fin_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_fin and gnomad_exome_AN_fin">
##INFO=<ID=gnomad_AN_oth_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_oth and gnomad_exome_AN_oth">
##INFO=<ID=gnomad_nhomalt_nfe_seu_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_nfe_seu and gnomad_exome_nhomalt_nfe_seu">
##INFO=<ID=gnomad_nhomalt_fin_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_fin_female and gnomad_exome_nhomalt_fin_female">
##INFO=<ID=gnomad_nhomalt_afr_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_afr_male and gnomad_exome_nhomalt_afr_male">
##INFO=<ID=gnomad_nhomalt_afr_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_afr and gnomad_exome_nhomalt_afr">
##INFO=<ID=gnomad_nhomalt_eas_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_eas_female and gnomad_exome_nhomalt_eas_female">
##INFO=<ID=gnomad_nhomalt_afr_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_afr_female and gnomad_exome_nhomalt_afr_female">
##INFO=<ID=gnomad_nhomalt_nfe_onf_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_nfe_onf and gnomad_exome_nhomalt_nfe_onf">
##INFO=<ID=gnomad_nhomalt_fin_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_fin_male and gnomad_exome_nhomalt_fin_male">
##INFO=<ID=gnomad_nhomalt_nfe_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_nfe_female and gnomad_exome_nhomalt_nfe_female">
##INFO=<ID=gnomad_nhomalt_amr_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_amr and gnomad_exome_nhomalt_amr">
##INFO=<ID=gnomad_nhomalt_eas_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_eas and gnomad_exome_nhomalt_eas">
##INFO=<ID=gnomad_nhomalt_asj_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_asj_male and gnomad_exome_nhomalt_asj_male">
##INFO=<ID=gnomad_nhomalt_oth_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_oth_female and gnomad_exome_nhomalt_oth_female">
##INFO=<ID=gnomad_nhomalt_nfe_nwe_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_nfe_nwe and gnomad_exome_nhomalt_nfe_nwe">
##INFO=<ID=gnomad_nhomalt_nfe_est_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_nfe_est and gnomad_exome_nhomalt_nfe_est">
##INFO=<ID=gnomad_nhomalt_eas_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_eas_male and gnomad_exome_nhomalt_eas_male">
##INFO=<ID=gnomad_nhomalt_nfe_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_nfe and gnomad_exome_nhomalt_nfe">
##INFO=<ID=gnomad_nhomalt_fin_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_fin and gnomad_exome_nhomalt_fin">
##INFO=<ID=gnomad_nhomalt_nfe_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_nfe_male and gnomad_exome_nhomalt_nfe_male">
##INFO=<ID=gnomad_nhomalt_asj_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_asj_female and gnomad_exome_nhomalt_asj_female">
##INFO=<ID=gnomad_nhomalt_asj_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_asj and gnomad_exome_nhomalt_asj">
##INFO=<ID=gnomad_nhomalt_oth_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_oth and gnomad_exome_nhomalt_oth">
##INFO=<ID=gnomad_nhomalt_amr_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_amr_male and gnomad_exome_nhomalt_amr_male">
##INFO=<ID=gnomad_nhomalt_amr_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_amr_female and gnomad_exome_nhomalt_amr_female">
##INFO=<ID=gnomad_nhomalt_oth_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_nhomalt_oth_male and gnomad_exome_nhomalt_oth_male">
##INFO=<ID=gnomad_nhomalt_nfe_bgr_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_nhomalt_nfe_bgr">
##INFO=<ID=gnomad_nhomalt_sas_male_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_nhomalt_sas_male">
##INFO=<ID=gnomad_nhomalt_sas_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_nhomalt_sas">
##INFO=<ID=gnomad_nhomalt_nfe_swe_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_nhomalt_nfe_swe">
##INFO=<ID=gnomad_nhomalt_eas_jpn_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_nhomalt_eas_jpn">
##INFO=<ID=gnomad_nhomalt_eas_kor_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_nhomalt_eas_kor">
##INFO=<ID=gnomad_nhomalt_eas_oea_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_nhomalt_eas_oea">
##INFO=<ID=gnomad_nhomalt_sas_female_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_nhomalt_sas_female">
##INFO=<ID=gnomad_AF_nfe_seu_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe_seu and gnomad_AN_nfe_seu">
##INFO=<ID=gnomad_AF_fin_female_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_fin_female and gnomad_AN_fin_female">
##INFO=<ID=gnomad_AF_afr_male_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_afr_male and gnomad_AN_afr_male">
##INFO=<ID=gnomad_AF_eas_female_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_eas_female and gnomad_AN_eas_female">
##INFO=<ID=gnomad_AF_afr_female_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_afr_female and gnomad_AN_afr_female">
##INFO=<ID=gnomad_AF_nfe_onf_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe_onf and gnomad_AN_nfe_onf">
##INFO=<ID=gnomad_AF_fin_male_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_fin_male and gnomad_AN_fin_male">
##INFO=<ID=gnomad_AF_nfe_female_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe_female and gnomad_AN_nfe_female">
##INFO=<ID=gnomad_AF_asj_male_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_asj_male and gnomad_AN_asj_male">
##INFO=<ID=gnomad_AF_oth_female_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_oth_female and gnomad_AN_oth_female">
##INFO=<ID=gnomad_AF_nfe_nwe_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe_nwe and gnomad_AN_nfe_nwe">
##INFO=<ID=gnomad_AF_nfe_est_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe_est and gnomad_AN_nfe_est">
##INFO=<ID=gnomad_AF_eas_male_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_eas_male and gnomad_AN_eas_male">
##INFO=<ID=gnomad_AF_nfe_male_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe_male and gnomad_AN_nfe_male">
##INFO=<ID=gnomad_AF_asj_female_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_asj_female and gnomad_AN_asj_female">
##INFO=<ID=gnomad_AF_amr_male_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_amr_male and gnomad_AN_amr_male">
##INFO=<ID=gnomad_AF_amr_female_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_amr_female and gnomad_AN_amr_female">
##INFO=<ID=gnomad_AF_oth_male_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_oth_male and gnomad_AN_oth_male">
##INFO=<ID=gnomad_AF_nfe_bgr_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe_bgr and gnomad_AN_nfe_bgr">
##INFO=<ID=gnomad_AF_sas_male_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_sas_male and gnomad_AN_sas_male">
##INFO=<ID=gnomad_AF_nfe_swe_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe_swe and gnomad_AN_nfe_swe">
##INFO=<ID=gnomad_AF_eas_jpn_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_eas_jpn and gnomad_AN_eas_jpn">
##INFO=<ID=gnomad_AF_eas_kor_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_eas_kor and gnomad_AN_eas_kor">
##INFO=<ID=gnomad_AF_eas_oea_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_eas_oea and gnomad_AN_eas_oea">
##INFO=<ID=gnomad_AF_sas_female_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_sas_female and gnomad_AN_sas_female">
##INFO=<ID=gnomad_AF_asj_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_asj and gnomad_AN_asj">
##INFO=<ID=gnomad_AF_fin_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_fin and gnomad_AN_fin">
##INFO=<ID=gnomad_AF_oth_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_oth and gnomad_AN_oth">
"""
gnomad_cols = []
pattern = r"<ID=gnomad_[\w]+,"
for match in re.findall(pattern, gnomad_string):
    gnomad_cols.append(match[4:-1])

gnomad_string = """##FILTER=<ID=gnomad_genome_PASS,Description="All filters passed">
##FILTER=<ID=gnomad_genome_AC0,Description="Allele count is zero after filtering out low-confidence genotypes (GQ < 20; DP < 10; and AB < 0.2 for het calls)">
##FILTER=<ID=gnomad_genome_InbreedingCoeff,Description="InbreedingCoeff < -0.3">
##FILTER=<ID=gnomad_genome_RF,Description="Failed random forest filtering thresholds of 0.2634762834546574, 0.22213813189901457 (probabilities of being a true positive variant) for SNPs, indels">
##FILTER=<ID=gnomad_exome_PASS,Description="All filters passed">
##FILTER=<ID=gnomad_exome_AC0,Description="Allele count is zero after filtering out low-confidence genotypes (GQ < 20; DP < 10; and AB < 0.2 for het calls)">
##FILTER=<ID=gnomad_exome_InbreedingCoeff,Description="InbreedingCoeff < -0.3">
##FILTER=<ID=gnomad_exome_RF,Description="Failed random forest filtering thresholds of 0.055272738028512555, 0.20641025579497013 (probabilities of being a true positive variant) for SNPs, indels">
##INFO=<ID=gnomad_AC_afr_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_afr and gnomad_exome_AC_afr">
##INFO=<ID=gnomad_AC_amr_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_amr and gnomad_exome_AC_amr">
##INFO=<ID=gnomad_AC_eas_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_eas and gnomad_exome_AC_eas">
##INFO=<ID=gnomad_AC_nfe_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AC_nfe and gnomad_exome_AC_nfe">
##INFO=<ID=gnomad_AC_sas_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AC_sas">
##INFO=<ID=gnomad_AN_afr_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_afr and gnomad_exome_AN_afr">
##INFO=<ID=gnomad_AN_amr_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_amr and gnomad_exome_AN_amr">
##INFO=<ID=gnomad_AN_eas_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_eas and gnomad_exome_AN_eas">
##INFO=<ID=gnomad_AN_nfe_pass,Number=A,Type=Integer,Description="Summation of gnomad_genome_AN_nfe and gnomad_exome_AN_nfe">
##INFO=<ID=gnomad_AN_sas_pass,Number=A,Type=Integer,Description="Summation of gnomad_exome_AN_sas">
##INFO=<ID=gnomad_AF_afr_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_afr and gnomad_AN_afr">
##INFO=<ID=gnomad_AF_amr_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_amr and gnomad_AN_amr">
##INFO=<ID=gnomad_AF_eas_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_eas and gnomad_AN_eas">
##INFO=<ID=gnomad_AF_nfe_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_nfe and gnomad_AN_nfe">
##INFO=<ID=gnomad_AF_sas_pass,Number=A,Type=Float,Description="Allele Frequency calculated from gnomad_AC_sas and gnomad_AN_sas">
##INFO=<ID=gnomad_MAX_MAF,Number=.,Type=Float,Description="Max MAF for gnomad, in range (0,1)">
##INFO=<ID=gnomad_MAX_MAF_SOURCE,Number=.,Type=String,Description="Max MAF population for gnomad">"""

for match in re.findall(pattern, gnomad_string):
    gnomad_cols.append(match[4:-1])


dbnsfp_string = """##INFO=<ID=DBNSFP_SIFT_PRED,Number=1,Type=String,Description="\"(from dbNSFP) If SIFTori is smaller than 0.05 (rankscore>0.39575) the corresponding nsSNV is predicted as D(amaging); otherwise it is predicted as T(olerated). Multiple predictions separated by ;\"">
##INFO=<ID=DBNSFP_SIFT_SCORE,Number=1,Type=String,Description="\"(from dbNSFP) SIFT score (SIFTori). Scores range from 0 to 1. The smaller the score the more likely the SNP has damaging effect. Multiple scores separated by ;, corresponding to Ensembl_proteinid.\"">
##INFO=<ID=DBNSFP_POLYPHEN2_HDIV_PRED,Number=1,Type=String,Description="\"(from dbNSFP) Polyphen2 prediction based on HumDiv, D (probably damaging, HDIV score in [0.957,1] or rankscore in [0.55859,0.91137]), P (possibly damaging, HDIV score in [0.454,0.956] or rankscore in [0.37043,0.55681]) and B (benign, HDIV score in [0,0.452] or rankscore in [0.03061,0.36974]). Score cutoff for binary classification is 0.5 for HDIV score or 0.38028 for rankscore, i.e. the prediction is neutral if the HDIV score is smaller than 0.5 (rankscore is smaller than 0.38028), and deleterious if the HDIV score is larger than 0.5 (rankscore is larger than 0.38028). Multiple entries are separated by ;, corresponding to Uniprot_acc.\"">
##INFO=<ID=DBNSFP_POLYPHEN2_HDIV_SCORE,Number=1,Type=String,Description="\"(from dbNSFP) Polyphen2 score based on HumDiv, i.e. hdiv_prob. The score ranges from 0 to 1. Multiple entries separated by ;, corresponding to Uniprot_acc.\"">
##INFO=<ID=DBNSFP_LRT_PRED,Number=1,Type=String,Description="\"(from dbNSFP) LRT prediction, D(eleterious), N(eutral) or U(nknown), which is not solely determined by the score.\"">
##INFO=<ID=DBNSFP_LRT_SCORE,Number=1,Type=String,Description="\"(from dbNSFP) The original LRT two-sided p-value (LRTori), ranges from 0 to 1.\"">
##INFO=<ID=DBNSFP_MUTATIONTASTER_PRED,Number=1,Type=String,Description="\"(from dbNSFP) MutationTaster prediction, A (disease_causing_automatic), D (disease_causing), N (polymorphism) or P (polymorphism_automatic). The score cutoff between D and N is 0.5 for MTnew and 0.31733 for the rankscore.\"">
##INFO=<ID=DBNSFP_MUTATIONTASTER_SCORE,Number=1,Type=String,Description="\"(from dbNSFP) MutationTaster p-value (MTori), ranges from 0 to 1. Multiple scores are separated by ;. Information on corresponding transcript(s) can be found by querying http://www.mutationtaster.org/ChrPos.html\"">
##INFO=<ID=DBNSFP_GERP_RS,Number=1,Type=String,Description="\"(from dbNSFP) GERP++ RS score, the larger the score, the more conserved the site. Scores range from -12.3 to 6.17.\"">
##INFO=<ID=DBNSFP_PHYLOP30WAY_MAMMALIAN,Number=1,Type=String,Description="\"(from dbNSFP) phyloP (phylogenetic p-values) conservation score based on the multiple alignments of 30 mammalian genomes (including human). The larger the score, the more conserved the site. Scores range from -20 to 1.312 in dbNSFP.\"">
##INFO=<ID=DBNSFP_INTERPRO_DOMAIN,Number=1,Type=String,Description="\"(from dbNSFP) domain or conserved site on which the variant locates. Domain annotations come from Interpro database. The number in the brackets following a specific domain is the count of times Interpro assigns the variant position to that domain, typically coming from different predicting databases. Multiple entries separated by ;.\"">
"""

dbnsfp_cols = []
pattern = r"<ID=DBNSFP_[\w]+,"
for match in re.findall(pattern, dbnsfp_string):
    dbnsfp_cols.append(match[4:-1])

definitely_keep_cols_from_thesis = ['NUM_PATH_PREDS', 'TOTAL_NUM_PREDS', 'FINAL_PRED', 'GENE', 'OVERALL_MAX_MAF', 'OVERALL_MAX_MAF_SOURCE', 'GENE', 'FINAL_PATHOGENICITY', 'CURATED_PATHOGENICITY', 'OTOSCOPE_MAX_MAF', 'OTOSCOPE_MAX_MAF_Source']
definitely_keep_from_ddg_data = ['Impact', 'CADD Phred', 'Interpro Domain', 'Max MAF (%)', 'Max MAF Source', 'Surface Area', 'Normalized SA', 'Confidence Score','ddG', '|ddG|',]
very_likely_kept = ['CLINVAR_PATHOGENIC', 'VEP_CADD_RAW', 'VEP_CADD_PHRED', 'VEP_SIFT_SCORE', 'VEP_SIFT_PRED', 'VEP_POLYPHEN_SCORE', 'VEP_POLYPHEN_PRED', 'MORL_MAX_MAF', 'MORL_MAX_MAF_SOURCE', ]
likely_kept_cls = ['CLINVAR_CLNSIG', 'VEP_CONSEQUENCE', 'VEP_IMPACT', 'VEP_IMPACT', 'VEP_FEATURE', 'FINAL_PATHOGENICITY_SOURCE', 'OTOSCOPE_MAX_MAF', 'OTOSCOPE_MAX_MAF_SOURCE',]
somewhat_likely_kept = ['CLINVAR_MAX_MAF', 'CLINVAR_CONFLICTED', ]
possible = ['UNIPROT_DOMAIN', ]
unknown = ['VEP_CANONICAL', 'VEP_PICK', 'VEP_IMPACT', 'VEP_FEATURE', 'FINAL_DISEASE', 'UNIPROT_DOMAIN_SOURCE', 'VEP_PROTEIN_POS', 'DBNSFP_GERP_RS_PRED', 'DBNSFP_PHYLOP30WAY_MAMMALIAN_PRED']
somewhat_likely_not_kept = ['CLINVAR_MAX_MAF_SOURCE', 'CLINVAR_HGMD_CONFLICTED', ]
likely_not_keep_cols = ['TYPE', 'CLINVAR_VID', 'CLINVAR_REVSTAT', 'CLINVAR_DISEASE', ] + ['CLINVAR_HGVS_C', 'CLINVAR_HGVS_P', 'CLINVAR_PMID', 'VEP_HGVS_P', 'VEP_HGVS_C', 'VEP_INTRON', 'VEP_EXON', ]
very_likely_not_keep_cols = ['VEP_OTHER_FEATURES']

kafeen_dvd_related = ['CLASSIFY_TRAIL', 'CLASSIFY_TRAIL_KEYS', 'FINAL_PMID_PRIMARY', 'FINAL_PMID', 'FINAL_COMMENTS', 'FINAL_PMID', 'FINAL_PATHOGENICITY_REASON', 'CURATED_DECISION_DATE', 'CURATED_PMID',  'CURATED_DISEASE', 'CURATED_COMMENTS', 'CURATED_UPDATE_VERSION', 'PREF_TRANSCRIPT']

# I think these are from the DDG data
could_not_find = ['Variant Classification', 'HGVS Nucleotide Change', 'HGVS Protein Change', 'Consequence', 'Phenotype', 'Exon', 'Intron', 'Protein Position', 'Impact', 'CADD Phred']

cols_to_drop = definitely_keep_cols_from_thesis + likely_not_keep_cols + likely_kept_cls + somewhat_likely_kept + very_likely_kept
cols_to_drop = cols_to_drop + somewhat_likely_not_kept + very_likely_not_keep_cols + unknown + kafeen_dvd_related + possible + could_not_find + definitely_keep_from_ddg_data
cols_to_drop = cols_to_drop + hgmd_cols + gnomad_cols + dbnsfp_cols

all_dfs.loc[:, ~all_dfs.columns.isin(cols_to_drop)].columns

# all_dfs.loc[[all_dfs.loc[:, ~all_dfs.columns.isin(cols_to_drop)]]

import csv
with open('feature_sorting.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Definitely Keep (used previously)'] + definitely_keep_cols_from_thesis)
    writer.writerow(['Definitely Keep (from ddG file)'] + definitely_keep_from_ddg_data)
    writer.writerow(['Very Likely Keep'] + very_likely_kept)
    writer.writerow(['Likely Keep'] + likely_kept_cls)
    writer.writerow(['Somewhat Likely Keep'] + somewhat_likely_kept)
    writer.writerow(["Possible"] + possible)
    writer.writerow(['Unknown'] + unknown)
    writer.writerow(['Somewhat Likely Not Keep'] + somewhat_likely_not_kept)
    writer.writerow(['Likely Not Keep'] + likely_not_keep_cols)
    writer.writerow(['Very Likely Not Keep'] + very_likely_kept)
    writer.writerow(['Kafeen or DVD Related'] + kafeen_dvd_related)
    writer.writerow(['Unlikely to keep (from ddG File)'] + could_not_find)
    writer.writerow(['HMGD Other Columns'] + hgmd_cols)
    writer.writerow(['gnomad Columns'] + gnomad_cols)
    writer.writerow(['DBNSFP Other Columns'] + dbnsfp_cols)