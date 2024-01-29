from cgi import test
from importlib.resources import path
from ntpath import join
from pickle import FALSE
from posixpath import split
import re
import csv
import pandas as pd

from icecream import ic
# BASE_DIR = '/Users/coltonmiller/CADD_Work/Regression/'

BASE_DIR = '/Users/seanryan/Documents/GitHub/MORL-DVD-SVM/'
REFS_DIR = f"{BASE_DIR}references/unzipped/"
OUTPUTS_DIR = f"{BASE_DIR}outputs/"

DVDTxtData = open(f'{REFS_DIR}DVDv9_e_20220220.ALLVARTYPES.arr.txt', 'r')
count = 0
data_points = []
for line in DVDTxtData:
    # if count > 10:
    #     break
    search = line
    #print(search)
    count = count + 1
    #matched = re.search("[\sACGT]+(?=[\s1-9.]+(?P<name>gnomad))", search)
    matched = re.search("(?<=\s)\d+(?=\s)", search)
    matched_Gene = re.search("(?P<name>GENE=[^;]*)", search)
    matched_Cadd = re.search("(?<=;)(?P<name>VEP_CADD_RAW=[^;]*)", search)
    matched_Maf = re.search("(?<=;)(?P<name>OVERALL_MAX_MAF=[^;]*)", search)
    matched_Patho = re.search("(?<=;)(?P<name>FINAL_PATHOGENICITY[^;]*)", search)
    matched_Disease = re.search("(?<=;)(?P<name>FINAL_DISEASE[^;]*)", search)

    temp_list=[]
    temp_list.append(search[0:2])
    if matched is not None :
        temp_list.append(matched.group(0))
    else :
        temp_list.append('XXXXX')
    if matched is not None :
        temp_list.append(matched.group(0))
    else :
        temp_list.append('XXXXXX')
    if matched_Gene is not None :
        temp_list.append(matched_Gene.group(0))
    else : 
        temp_list.append('GENE=XXXXXX')
    if matched_Cadd is not None :
        temp_list.append(matched_Cadd.group(0))
    else :
        temp_list.append('VEP_CADD_RAW=XXXXXX')
    if matched_Maf is not None :
        temp_list.append(matched_Maf.group(0))
    else :
        temp_list.append('OVERALL_MAX_MAF=XXXXXX')
    if matched_Patho is not None :
        temp_list.append(matched_Patho.group(0))
    else :
        temp_list.append('FINAL_PATHOGENICITY=XXXXXX')
    if matched_Disease is not None :
        temp_list.append(matched_Disease.group(0))
    else :
        temp_list.append('FINAL_DISEASE=XXXXXX')

    data_points.append(temp_list)
    count += 1

allVariantsToCSV = []
for element in data_points:
    elementStr = ",".join(element)
    allVariantsToCSV.append(elementStr)

with open(f'{OUTPUTS_DIR}AllVariantsData20230330.txt','w') as testfile:
    for row in allVariantsToCSV:
        testfile.write(row + '\n')
        
        
########################

# TODO-RECENT WORK
allVariantData = open(f'{REFS_DIR}AllVariantsData20230330.txt', 'r')
count = 0
data_points = [] 
for line in allVariantData:
    line = line.strip()
    split_line = re.split(",", line)
    split_line[0] = split_line[0].replace('\t', '')
    index = 2
    del split_line[2]
    data_points.append(split_line)
print(data_points)

diseaseTags = open(f'{BASE_DIR}FinalDiseaseTypesUnique-HA.csv', 'r')
disease_points = []
for line in diseaseTags:
    disease_points.append(line)
trimmed_disease_points = []
for x in disease_points:
    trimmed_element = x.replace("\n", "");
    trimmed_disease_points.append(trimmed_element)
# print(trimmed_disease_points)

matched_disease_points = []
for i in data_points:
    string_to_compare_disease = i[6];
    trimmed_string_to_compare_disease = string_to_compare_disease.replace("FINAL_DISEASE=", "");
    for j in trimmed_disease_points:
        if(trimmed_string_to_compare_disease == j):
            matched_disease_points.append(i)
            break;

print(matched_disease_points)
print(len(matched_disease_points))
print(len(data_points))
allVariantsToCSV = []
for element in matched_disease_points:
    elementStr = ",".join(element)
    allVariantsToCSV.append(elementStr)

with open(f'{OUTPUTS_DIR}MatchedDiseaseVariantsData20230330.txt', 'w') as testfile:
    for row in allVariantsToCSV:
        testfile.write(row + '\n')

########################

DVDTxtData = open(f'{REFS_DIR}20220403LikelyBenignVariants.txt', 'r')
count = 0
data_points = []
for line in DVDTxtData:
    # if count > 10:
    #     break
    search = line
    #print(search)
    count = count + 1
    #matched = re.search("[\sACGT]+(?=[\s1-9.]+(?P<name>gnomad))", search)
    matched = re.search("(?<=\s)\d+(?=\s)", search)
    matched_Gene = re.search("(?P<name>GENE=[^;]*)", search)
    matched_Cadd = re.search("(?<=;)(?P<name>VEP_CADD_RAW=[^;]*)", search)
    matched_Maf = re.search("(?<=;)(?P<name>OVERALL_MAX_MAF=[^;]*)", search)
    matched_Patho = re.search("(?<=;)(?P<name>FINAL_PATHOGENICITY[^;]*)", search)
    matched_Disease = re.search("(?<=;)(?P<name>FINAL_DISEASE[^;]*)", search)

    temp_list=[]
    temp_list.append(search[0:2])
    if matched is not None :
        temp_list.append(matched.group(0))
    else :
        temp_list.append('XXXXX')
    if matched is not None :
        temp_list.append(matched.group(0))
    else :
        temp_list.append('XXXXXX')
    if matched_Gene is not None :
        temp_list.append(matched_Gene.group(0))
    else : 
        temp_list.append('GENE=XXXXXX')
    if matched_Cadd is not None :
        temp_list.append(matched_Cadd.group(0))
    else :
        temp_list.append('VEP_CADD_RAW=XXXXXX')
    if matched_Maf is not None :
        temp_list.append(matched_Maf.group(0))
    else :
        temp_list.append('OVERALL_MAX_MAF=XXXXXX')
    if matched_Patho is not None :
        temp_list.append(matched_Patho.group(0))
    else :
        temp_list.append('FINAL_PATHOGENICITY=XXXXXX')
    if matched_Disease is not None :
        temp_list.append(matched_Disease.group(0))
    else :
        temp_list.append('FINAL_DISEASE=XXXXXX')

    data_points.append(temp_list)
    count += 1

allVariantsToCSV = []
for element in data_points:
    elementStr = ",".join(element)
    allVariantsToCSV.append(elementStr)

with open(f'{OUTPUTS_DIR}LBVariantsData20230330.txt','w') as testfile:
    for row in allVariantsToCSV:
        testfile.write(row + '\n')

########################

allVariantData = open(f'{BASE_DIR}LBVariantsData20230330.txt', 'r')
count = 0
data_points = [] 
for line in allVariantData:
    line = line.strip()
    split_line = re.split(",", line)
    split_line[0] = split_line[0].replace('\t', '')
    index = 2
    del split_line[2]
    data_points.append(split_line)
print(data_points)

########################

diseaseTags = open(f'{BASE_DIR}FinalDiseaseTypesUnique-HA.csv', 'r')
disease_points = []
for line in diseaseTags:
    disease_points.append(line)
trimmed_disease_points = []
for x in disease_points:
    trimmed_element = x.replace("\n", "");
    trimmed_disease_points.append(trimmed_element)
# print(trimmed_disease_points)

matched_disease_points = []
for i in data_points:
    string_to_compare_disease = i[6];
    trimmed_string_to_compare_disease = string_to_compare_disease.replace("FINAL_DISEASE=", "");
    for j in trimmed_disease_points:
        if(trimmed_string_to_compare_disease == j):
            matched_disease_points.append(i)
            break;

print(matched_disease_points)
print(len(matched_disease_points))
print(len(data_points))
allVariantsToCSV = []
for element in matched_disease_points:
    elementStr = ",".join(element)
    allVariantsToCSV.append(elementStr)

with open(f'{OUTPUTS_DIR}LBMatchedDiseaseVariantsData20230330.txt', 'w') as testfile:
    for row in allVariantsToCSV:
        testfile.write(row + '\n')
        
########################

cleanedAllVariatnsToCSV = []
for element in data_points:
    elementStr=",".join(element)
    cleanedAllVariatnsToCSV.append(elementStr)

with open(f'{OUTPUTS_DIR}CleanedAllVariantsData20230118.txt','w') as testfile:
    for row in cleanedAllVariatnsToCSV:
        testfile.write(row + '\n')
        
########################

DVDTxtData = open(f'{REFS_DIR}DVDv9_e_20220220.ALLVARTYPES.arr.txt', 'r')
count = 0
data_points = []

for line in DVDTxtData:
    # if count > 20:
    #     break
    line = line.strip()
    split_line = re.split("\t", line)
    final_split_line = split_line[0:5]
    find_index = [0,1,3,4]
    cut_final_split_line = [final_split_line[i] for i in find_index]
    #print(cut_final_split_search)
    joined_split_line = "\t".join(cut_final_split_line)
    #print(joined_split_line)
    data_points.append(joined_split_line)
    count+=1
print(data_points)
cleanedAllProteinConvertingPointsToCSV = []

########################

with open(f'{OUTPUTS_DIR}/CleanedProteinPointsConvert20230118.tsv','w') as testfile:
    for row in data_points:
        testfile.write(row + '\n')
    split_search = re.split("\t", search)
    final_split_search = split_search[0:5]
    find_index = [0,1,3,4]
    cut_final_split_search = [final_split_search[i] for i in find_index]
    #print(final_split_search)
    #print(cut_final_split_search)
    joined_split_search = "\t".join(cut_final_split_search)
    #print(joined_split_search)
    data_points.append(joined_split_search)
    
########################

CleanedVariantTxtData = open(f'{BASE_DIR}CleanedAllVariantsData20230118.txt', 'r')
print(CleanedVariantTxtData)
count = 0
data_points = []
for line in CleanedVariantTxtData:
    line = line.strip()
    split_line = re.split(",",line)
    split_line[2] = split_line[2][5:]
    split_line[3] = split_line[3][13:]
    split_line[4] = split_line[4][16:]
    split_line[5] = split_line[5][20:]
    joined_split_line = ",".join(split_line)
    data_points.append(joined_split_line)
    
########################

print(data_points)
with open(f'{OUTPUTS_DIR}ProcessedCleanedAllVariantDataPoints20230118.txt', 'w') as testfile:
    for row in data_points:
        testfile.write(row +'\n')
        
########################


# ProteinCoordData = open(f'{REFS_DIR}AllVariantsResults20230118.tsv', 'r')
ProteinCoordData = open(f'{REFS_DIR}AllVariantsResults.tsv', 'r')


proteinCoords = []
count = 0
# with open(f'{BASE_DIR}AllVariantsResults20230318.tsv') as f:
with open(f'{REFS_DIR}AllVariantsResults.tsv') as f:
    for line in f:
        temp = []
        #l = line.split('\t')
        split_search_protein_coord = re.split("\t", line)
        find_index_protein_coord = [0,1,6,25]
        cut_final_split_search_protein_coord = [split_search_protein_coord[j] for j in find_index_protein_coord]
        joined_protein_coord_split_search = ",".join(cut_final_split_search_protein_coord)
        proteinCoords.append(joined_protein_coord_split_search)
        
########################

ic(proteinCoords)
count_1 = 0


for i in proteinCoords:
    ic(i)
    print(len(i))
    if count_1<20:
        print(i[0] +","+ i[1]+"," + i[6]+"," + i[25])
        #print(i)
        count_1 = count_1 + 1
    else:
        break

proteinCoords_df = pd.read_csv(f'{BASE_DIR}results.tsv', sep='\t')
read_tsv = csv.reader(ProteinCoordData, delimiter = "\t")
for row in read_tsv:
    print(row)
print(count)
print(data_points)
    

########################
 
pathogenic_Benign_Dataset = []

for record in data_points:
    if record[5] == 'FINAL_PATHOGENICITY=Pathogenic' or record[5] == 'FINAL_PATHOGENICITY=Benign':
        pathogenic_Benign_Dataset.append(record)


with open(f'{OUTPUTS_DIR}Missense_data_points.txt', 'w') as testfile:
    for row in data_points:
        testfile.write(' '.join([str(a) for a in row]) + '\n')

########################

with open(f'{OUTPUTS_DIR}Missense_data_point_benignORpathogenic.txt','w') as testfile2:
    for row in pathogenic_Benign_Dataset:
        testfile2.write(' '.join([str(a) for a in row]) +'\n')

with open(f'{OUTPUTS_DIR}Protein_Coord_All_data_points.txt','w') as testfile:
    for row in proteinCoords:
        testfile.write(row + '\n')
        
########################

variantsDataFile = open(f'{BASE_DIR}ProcessedCleanedAllVariantDataPoints.txt',"r")
lines = variantsDataFile.read().splitlines()
variantsData2D = []
for k in lines:
    arrVariantPoint = []
    arrVariantPoint = ",".join(k.split())
    arrVariantPoint = arrVariantPoint.split(sep=",")
    variantsData2D.append(arrVariantPoint)

variantsDataFile.close()

########################

# print(variantsData2D)

proteinCoordsDataFile = open(f'{BASE_DIR}Protein_Coord_All_data_points.txt',"r")
lines = proteinCoordsDataFile.read().splitlines()
proteinCoordData2D = []
for l in lines:
    arrProteinCoordDataPoint = []
    arrProteinCoordDataPoint = l.split(sep=",")
    proteinCoordData2D.append(arrProteinCoordDataPoint)

proteinCoordsDataFile.close()
# print(proteinCoordData2D)

########################

count = 0
for p in proteinCoordData2D:
    for m in variantsData2D:
        if m[0] == p[0] and m[1] == p[1] and m[2] == p[2]:
            m.append(p[3])


variantsWithProteinCoordsToCSV = []
for element in variantsData2D:
    elementStr = ",".join(element)
    variantsWithProteinCoordsToCSV.append(elementStr)

print(variantsWithProteinCoordsToCSV)

# #print(missenseData2D)

with open(f'{OUTPUTS_DIR}AllVariantsWithProteinPos.txt','w') as testfile:
    for row in variantsWithProteinCoordsToCSV:
        testfile.write(row + '\n')

########################

dataToClean = open(f'{BASE_DIR}domainsToEditWithClass.csv',"r")
lines = dataToClean.read().splitlines()
resultsWithCleanedDomain2D = []
for l in lines:
    arrGeometricProteinCoordDataPoint = []
    arrGeometricProteinCoordDataPoint = l.split(sep=",")
    resultsWithCleanedDomain2D.append(arrGeometricProteinCoordDataPoint)

print(resultsWithCleanedDomain2D)
for element in resultsWithCleanedDomain2D:
    if element[10] == 'None':
        element[10] = '0'
    else:
        element[10] = '1'
print(resultsWithCleanedDomain2D)

processedWFS1ValidMissenseGeometricWithDomainProteinDataPointsToCSV = []
for element in resultsWithCleanedDomain2D:
    elementStr = ",".join(element)
    processedWFS1ValidMissenseGeometricWithDomainProteinDataPointsToCSV.append(elementStr)
#print(processedValidMissenseGeometricProteinDataPointsToCSV)
with open(f'{OUTPUTS_DIR}CleanedWFS1DomainDataWithClass.csv','w') as testfile:
    for row in processedWFS1ValidMissenseGeometricWithDomainProteinDataPointsToCSV:
        testfile.write(row + '\n')

########################

import os
import numpy as np

# # # proteinCoordsDataFile = open(f'{BASE_DIR}Protein_Coord_data_points.txt',"r")
# # # lines = proteinCoordsDataFile.read().splitlines()
# # # proteinCoordData2D = []
# # # for l in lines:
# # #     arrProteinCoordDataPoint = []
# # #     arrProteinCoordDataPoint = l.split(sep=",")
# # #     proteinCoordData2D.append(arrProteinCoordDataPoint)
# directory = '/Users/coltonmiller/CADD_Work/csv_wConfidence'
directory = f"{OUTPUTS_DIR}csv_with_confidence/"


for root, dirs, files in os.walk(directory):
    
    for filename in files:
        count = 0
        geometricArray=[]
        filePath = os.path.join(root,filename)
        filename = filePath
        matched = re.search("\w+(?:\.csv)", filename)
        gene_name_csv = matched.group(0)
        gene_name = gene_name_csv[:-4]
        with open(filename,'r') as csvfile:
            print(filename)
            for line in csvfile:
                temp = []
                line = line.strip()
                line = line.split('\t')
                #print(line)
                if count != 0:
                    line.append(gene_name)
                else:
                    line.append('GENE')
                geometricArray.append(line)
                count += 1
        print(geometricArray)
        geometricArrayToCSV = []
        
        for row in geometricArray:
            rowStr = ",".join(row)
            geometricArrayToCSV.append(rowStr)
        outputGeometricCSVDir = '/Users/coltonmiller/CADD_Work/geneCsv_wConfidence/'
        fileText = outputGeometricCSVDir+gene_name_csv
        with open(fileText,'w') as testfile:
            for row in geometricArrayToCSV:
                testfile.write(row + '\n')
        testfile.close()

########################

import glob, os
import pandas as pd

path = '/Users/coltonmiller/CADD_Work/featureMappedCsvs/'
all_files = glob.glob(os.path.join(path, "*.csv"))
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
df_merged   = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv( "/Users/coltonmiller/CADD_Work/merged_csv_wConfidenceDDG.csv")

files = os.path.join('/Users/coltonmiller/CADD_Work/featureMappedCsvs/', "*.csv")
files = glob.glob(files)
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
print(df)

########################

import glob, os
import pandas as pd


########################
path = '/Users/coltonmiller/CADD_Work/newCSVs/'
all_files = glob.glob(os.path.join(path, "*.csv"))
df_from_each_file = (pd.read_csv(f, sep=',') for f in all_files)
df_merged = pd.concat(df_from_each_file, ignore_index=True)
df_merged.to_csv("/Users/coltonmiller/CADD_Work/merged_csv_wFreeEnergies.csv")

########################

freeEnergyDataFile = open("/Users/coltonmiller/CADD_Work/merged_csv_wFreeEnergies.csv","r")
lines = freeEnergyDataFile.read().splitlines()
freeEnergyData2D = []
for l in lines:
    #print(l)
    arrGeometricFreeEnergyDataPoint = []
    arrGeometricFreeEnergyDataPoint = l.split(sep=",")
    freeEnergyData2D.append(arrGeometricFreeEnergyDataPoint)
trimmedFreeEnergyData2D = []

for row in freeEnergyData2D:
    if(len(row)>2):
        temp = []
        temp.append(row[1])
        flag = False
        for element in row:
            if flag:
                temp.append(element)
                flag = False
            if element == 'MODERATE':
                flag = True
        trimmedFreeEnergyData2D.append(temp)

coordinates2D = []
#print(trimmedFreeEnergyData2D)
for row in trimmedFreeEnergyData2D:
    temp = []
    split_row = row[0].split(sep=":")
    temp.append(split_row[0])
    temp.append(split_row[1])
    if(len(row) > 1):
        temp.append(row[1])
        #print(row)
    #temp.append(row[1])
    coordinates2D.append(temp)
#print(coordinates2D)

########################

existing_dataPoints = open("/Users/coltonmiller/CADD_Work/Regression/ValidProcessedValidMissenseWithGeometricAndDomainData.csv","r")
data_lines = existing_dataPoints.read().splitlines()
existing_dataPoints2D = []
for l in data_lines:
    arrExistingDataPoint = []
    arrExistingDataPoint = l.split(sep=",")
    existing_dataPoints2D.append(arrExistingDataPoint)
#print(existing_dataPoints2D)

validProcessedMissenseWithFreeEnergyGeometricAndDomainData = []
for j in existing_dataPoints2D:
    for k in coordinates2D:
        if k[0] == j[0] and k[1] == j[1]:
            temp = []
            j.append(k[2])
            #print(j)

            # temp_row = j.split(sep=',')
            # temp.append(temp_row)
            # temp.append(k[2])
            validProcessedMissenseWithFreeEnergyGeometricAndDomainData.append(j)
#print(validProcessedMissenseWithFreeEnergyGeometricAndDomainData)

# test_array = [1,2,3,4,5,6,7]
# print(len(test_array))
# count = 2
# print(test_array[-count])

# test_array = test_array[0:2]
# print(test_array)
validProcessedMissenseWithFreeEnergyGeometricAndDomainAverageData = []
for item in validProcessedMissenseWithFreeEnergyGeometricAndDomainData:
    #validProcessedMissenseWithFreeEnergyGeometricAndDomainTrimmedData.append(item[0:16])
    if len(item) > 16:
        sum = 0
        count = 1
        while count <= (len(item) - 15):
            if str(item[-count]) == '':
                count += 1
            sum += float(item[-count])
            count += 1
        average_free_energy = sum/count
        temp = item[0:15]
        temp.append(str(average_free_energy))
        validProcessedMissenseWithFreeEnergyGeometricAndDomainAverageData.append(temp)
    else:
        validProcessedMissenseWithFreeEnergyGeometricAndDomainAverageData.append(item)

# print(validProcessedMissenseWithFreeEnergyGeometricAndDomainAverageData)

validProcessedMissenseWithFreeEnergyGeometricAndDomainAverageDataToCSV = []
for element in validProcessedMissenseWithFreeEnergyGeometricAndDomainAverageData:
    elementStr = ",".join(element)
    validProcessedMissenseWithFreeEnergyGeometricAndDomainAverageDataToCSV.append(elementStr)

with open('ValidProcessedValidMissenseWithFreeEnergyGeometricAndDomainData.csv','w') as testfile:
    for row in validProcessedMissenseWithFreeEnergyGeometricAndDomainAverageDataToCSV:
        testfile.write(row + '\n')
testfile.close()




    
print(trimmedFreeEnergyData2D)

########################

# import pandas as pd
# df = pd.read_csv("/Users/coltonmiller/CADD_Work/merged_csv_wConfidence.csv")
# first_column = df.columns[0]
# df = df.drop([first_column], axis = 1)
# df.to_csv("/Users/coltonmiller/CADD_Work/merged_csv_wConfidence.csv", index = False)


missenseAndProteinCoordsDataFile = open(f'{BASE_DIR}MissenseWithProteinPos.txt',"r")
lines = missenseAndProteinCoordsDataFile.read().splitlines()
missenseAndProteinCoordData2D = []
for l in lines:
    arrMissenseAndProteinCoordDataPoint = []
    arrMissenseAndProteinCoordDataPoint = l.split(sep=",")
    missenseAndProteinCoordData2D.append(arrMissenseAndProteinCoordDataPoint)

missenseAndProteinCoordsDataFile.close()

trimmedMissenseAndProteinCoordData2D = []
for row in missenseAndProteinCoordData2D:
    row = row[0:7]
    trimmedMissenseAndProteinCoordData2D.append(row)
#print(trimmedMissenseAndProteinCoordData2D)

########################

geometricProteinCoordsDataFile = open('/Users/coltonmiller/CADD_Work/merged_csv_wConfidence.csv',"r")
lines = geometricProteinCoordsDataFile.read().splitlines()
geometricProteinCoordData2D = []
for l in lines:
    arrGeometricProteinCoordDataPoint = []
    arrGeometricProteinCoordDataPoint = l.split(sep=",")
    geometricProteinCoordData2D.append(arrGeometricProteinCoordDataPoint)

geometricProteinCoordsDataFile.close()
#print(geometricProteinCoordData2D)
#print(geometricProteinCoordData2D[0][5:11])

########################

missenseWithGeometricData2D = []

count = 0
for m in trimmedMissenseAndProteinCoordData2D:
    # if count > 50:
    #     break
    # count += 1
    for g in geometricProteinCoordData2D:
        gene_name = m[2][5:]
        #print(gene_name)
        if gene_name == g[11] and m[6] == g[1]:
            m.append(g[5])
            m.append(g[6])
            m.append(g[7])
            m.append(g[8])
            m.append(g[9])
            m.append(g[10])
   # print(m)

missenseWithGeometricDataToCSV = []
for element in trimmedMissenseAndProteinCoordData2D:
    elementStr = ",".join(element)
    missenseWithGeometricDataToCSV.append(elementStr)

# print(missenseWithGeometricDataToCSV)

# # #print(missenseData2D)

with open('MissenseWithGeometricData.txt','w') as testfile:
    for row in missenseWithGeometricDataToCSV:
        testfile.write(row + '\n')
testfile.close()

########################

missenseGeometricData = []
missenseGeometricDataFile = open(f'{BASE_DIR}MissenseWithGeometricData.txt',"r")
lines = missenseGeometricDataFile.read().splitlines()
trimmedMissenseGeometricData2D = []
for l in lines:
    arrMissenseGeometricPoint = []
    arrMissenseGeometricPoint = l.split(sep=",")
    trimmedMissenseGeometricData2D.append(arrMissenseGeometricPoint)

#print(trimmedMissenseGeometricData2D)

validGeometricDataPoints = []
for element in trimmedMissenseGeometricData2D:
    length = len(element)
    if length > 9:
        validGeometricDataPoints.append(element)

#print(validGeometricDataPoints)
trimmedValidGeometricDataPoints = []
for element in validGeometricDataPoints:
    element[2] = element[2][5:]
    element[3] = element[3][13:]
    element[4] = element[4][16:]
    element[5] = element[5][20:]
    trimmedValidGeometricDataPoints.append(element)

trimmedValidGeometricDataPointsToCSV = []
for element in trimmedValidGeometricDataPoints:
    elementStr = ",".join(element)
    trimmedValidGeometricDataPointsToCSV.append(elementStr)

print(trimmedValidGeometricDataPointsToCSV)

with open('ValidMissenseWithGeometricData.txt','w') as testfile:
    for row in trimmedValidGeometricDataPointsToCSV:
        testfile.write(row + '\n')
testfile.close()

########################

validGeometricProteinData = []
validMissenseGeometricProteinDataFile = open(f'{BASE_DIR}ValidMissenseWithGeometricData.txt',"r")
lines = validMissenseGeometricProteinDataFile.read().splitlines()
processedValidMissenseGeometricProteinData2D = []
for l in lines:
    arrValidMissenseGeometricPoint = []
    arrValidMissenseGeometricPoint = l.split(sep=",")
    processedValidMissenseGeometricProteinData2D.append(arrValidMissenseGeometricPoint)

for element in processedValidMissenseGeometricProteinData2D:
    if element[4] == ".":
        element[4] = '0.0000'
    if element[5] == 'Pathogenic':
        element.append('1')
    else:
        element.append('0')
    if element[7] == NULL:
        print('Null found: 7')
    if element[8] == NULL:
        print('Null found: 8')
    if element[9] == NULL:
        print('Null found: 9')
print(processedValidMissenseGeometricProteinData2D)
processedValidMissenseGeometricProteinDataPointsToCSV = []
for element in processedValidMissenseGeometricProteinData2D:
    elementStr = ",".join(element)
    processedValidMissenseGeometricProteinDataPointsToCSV.append(elementStr)
#print(processedValidMissenseGeometricProteinDataPointsToCSV)

with open('ProcessedValidMissenseWithGeometricData.csv','w') as testfile:
    for row in processedValidMissenseGeometricProteinDataPointsToCSV:
        testfile.write(row + '\n')
testfile.close()

########################

processedValidMissenseGeometricProteinDataFile = open(f'{BASE_DIR}ProcessedValidMissenseWithGeometricData.csv',"r")
lines = processedValidMissenseGeometricProteinDataFile.read().splitlines()
finalProcessedValidMissenseGeometricProteinData2D = []
for l in lines:
    arrProcessedValidMissenseGeometricPoint = []
    arrProcessedValidMissenseGeometricPoint = l.split(sep=",")
    finalProcessedValidMissenseGeometricProteinData2D.append(arrProcessedValidMissenseGeometricPoint)

count = 0
for element in finalProcessedValidMissenseGeometricProteinData2D:
    if count>0:
        element[4] = float(element[4])
        count+=1

print(finalProcessedValidMissenseGeometricProteinData2D)

########################

domainBedFile = open(f'{BASE_DIR}unipDomain.slim.bed')
lines = domainBedFile.read().splitlines()
domainBed2D = []
for l in lines:
    arrBedDataPoint = []
    arrBedDataPoint = l.split(sep="\t")
    domainBed2D.append(arrBedDataPoint)

#print(domainBed2D)

########################

processedValidMissenseGeometricProteinDataFile = open(f'{BASE_DIR}MissingMAFProcessedValidMissenseWithGeometricData.csv')
lines = processedValidMissenseGeometricProteinDataFile.read().splitlines()
data2D = []
for l in lines:
    arrDataPoint = []
    arrDataPoint = l.split(sep=",")
    data2D.append(arrDataPoint)
#print(data2D)

########################

mergedDDGDataFile = open('merged_DDGData.csv')
lines = mergedDDGDataFile.read().splitlines()
data2D = []
for l in lines:
    arrDataPoint = []
    arrDataPoint = l.split(sep=",")
    data2D.append(arrDataPoint)

for i in data2D:
    if len(i) > 19:
        print(i)
print("hi")

########################

modifiedMergedDDGDataFile = open('modified_merged_DDGData.csv')
lines = modifiedMergedDDGDataFile.read().splitlines()
data2D = []
for l in lines:
    arrDataPoint = []
    arrDataPoint = l.split(sep=",")
    data2D.append(arrDataPoint[0])
print(data2D)
with open('ddg_coords.csv','w') as testfile:
    for row in data2D:
        row = row.replace('"', '')
        row = row.replace(':', ' ')
        row = row.replace('>', ' ')
        testfile.write(row + '\n')
testfile.close()

########################

tsv_to_csv_File = open('results.tsv')
lines = tsv_to_csv_File.read().splitlines()
dataTSV = []
for l in lines:
    arrDataPoint = []
    arrDataPoint = l.split(sep="\t")
    temp = []
    temp.append(arrDataPoint[0])
    temp.append(arrDataPoint[1])
    temp.append(arrDataPoint[6])
    dataTSV.append(temp)
print(dataTSV)

########################

# TODO- KeEP THIS
modifiedMergedDDGDataFile = open('modified_merged_DDGData.csv')
lines = modifiedMergedDDGDataFile.read().splitlines()
data2D = []
locations2D = []
for l in lines:
    arrDataPoint = []
    arrDataPoint = l.split(sep=",")
    locationArr = []
    locationArr = arrDataPoint[0].split(sep=':')
    locationArr[0] = locationArr[0].replace('"', '')
    locations2D.append(locationArr)
    data2D.append(arrDataPoint)
print(locations2D)
count = 0
prevGene = dataTSV[0][2]
print(prevGene)
counti = 0
for i in dataTSV:
    counti += 1
    if counti > 22000:
        break
    else:
        if i[2] != prevGene:
            print(str(prevGene) + ": " + str(count))
            prevGene = i[2]
            count = 0
        else:
            count += 1
        
#TODO
# USH2A: 4k 90%
# TRIOBP: 2k 88%
# TECTA: 1500 87%
# OTOG: 2k 85%
# MYO7A: 2k 86%
# MYO15A: 3k 88%
# LRP2: 2.8k 85%
# KMT2D: 3.5k 89%
# COL11A1: 1.9k 83%
# CHD7: 1.8k 84%
# BDP1: 1.6k 81%


print(data2D)

print(len(data2D))
print(len(dataTSV))
for j in data2D:
    for i in dataTSV:
        locationArr = []
        locationArr = j[0].split(sep=':')
        locationArr[0] = locationArr[0].replace('"','')
        #print(locationArr)
        if str(i[0]) == locationArr[0]:
            if str(i[1]) == locationArr[1]:
                print('MATCH: ' + str(count))
                count += 1
                arrDataPoint = []
                # arrDataPoint=i.split(sep=",")
                temp = []
                temp.append(j)
                temp.append(str(i[2]))
                ddg_with_Genes.append(temp)
print(ddg_with_Genes)

with open('ddg_values_with_gene.csv','w') as testfile:
    for row in ddg_with_Genes:
        testfile.write(row + '\n')
testfile.close()
print(data2D)

for j in data2D:
    match = 0
    for i in domainBed2D:
        if j[0] == i[0]:
            if j[1] > i[1] and j[1] < i[2]:
                #j.append[i[3]]
                matched_domain = i[3]
                match = 1
    if match == 1:
        j.append(matched_domain)
    else:
        j.append('None')

#print(data2D)

########################

processedValidMissenseGeometricWithDomainProteinDataPointsToCSV = []
for element in data2D:
    elementStr = ",".join(element)
    processedValidMissenseGeometricWithDomainProteinDataPointsToCSV.append(elementStr)
#print(processedValidMissenseGeometricProteinDataPointsToCSV)

with open('ValidProcessedValidMissenseWithGeometricAndDomainData.csv','w') as testfile:
    for row in processedValidMissenseGeometricWithDomainProteinDataPointsToCSV:
        testfile.write(row + '\n')
testfile.close()

########################

with open(filename, 'r') as csvfile:
    
    print(gene_name)
    for line in csvfile:
        temp = []
        line = line.split('\t')
        line.append(gene_name)
        
        
        #split_search_geometric_coord = re.split("\t", line)
        geometricArray.append(line)


print(geometricArray)

########################

count = 0
for filename in os.scandir(directory):
    print(filename)
    print(directory+filename)
    if filename.is_file():
        
        with open(directory+filename) as csvfile:
            geometricArray = np.loadtxt(filename, delimiter=",")
        print(geometricArray)
    break
print(count)
print(data_points)

########################

import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
import sklearn.metrics as metric
# %matplotlib inline
raw_data = pd.read_csv("merged_DDGData.csv")
print(raw_data)



print(data_points)
print('Count: {}', count)
print(matched_Gene.group(0))
print(matched_Cadd.group(0))
print(matched_Phred.group(0))
#print(matched_Maf.group(0))
print(matched_Patho.group(0))
print('Chrom: {}, Pos: {} CADD: {}, PHRED: {}, MAF: {}, PATHO: {}', matched.group(0), matched_Cadd.group(0), matched_Phred.group(0), matched_Maf.group(0), matched_Patho.group(0))
# "(?<=\s)\d+(?=\s)"m
# "(?<=;)(?P<name>VEP_CADD_RAW=[^;]*)"m
# "(?<=;)(?P<name>VEP_CADD_PHRED=[^;]*)"m
# "(?<=;)(?P<name>OVERALL_MAX_MAF=)\d+\.\d+"m
# "(?<=;)(?P<name>FINAL_PATHOGENICITY=[a-zA-Z]+)"m
# (?<=\s)\d+(?=\s)
# (?P<name>OVERALL_MAX_MAF[^;]*)
# with open("FinalDiseaseTypesDistinct.txt","r")as f:

########################