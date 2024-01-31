#!/bin/bash

# Download OtoProtein from GitHub
curl -L https://github.com/SchniedersLab/OtoProtein/archive/master.zip -o OtoProtein.zip

unzip OtoProtein.zip

# Find all the files with an extension that is not .csv and remove them
find OtoProtein-master -type f ! -name '*.csv' -exec rm {} +

# Find all the csv files and execute a shell command to move them up one directory
find OtoProtein-master -name "*.csv" -exec sh -c 'mv "$1" "$(dirname "$1")"/..' _ {} \;

# Remove all the subdirectories
find OtoProtein-master -mindepth 1 -type d -depth -exec rm -r {} \;

# Remove the first line of each file
find OtoProtein-master -name "*.csv" -exec sed -i '' '1d' {} \;

# Remove the OtoProtein zip file
rm OtoProtein.zip

mv OtoProtein-master featureMappedCsvs