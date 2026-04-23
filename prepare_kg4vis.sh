#!/bin/bash

# prepare data for KG4Vis

curl https://kg4vis.s3.us-east-2.amazonaws.com/corpus.zip -o corpus.zip
unzip corpus.zip

curl https://kg4vis.s3.us-east-2.amazonaws.com/feature.zip -o feature.zip
unzip feature.zip

# move the file to KG4Vis folder
mv raw_data_all.csv vendor/KG4Vis/data
mv feature_test.csv vendor/KG4Vis/features
mv feature_train.csv vendor/KG4Vis/features

rm corpus.zip
rm feature.zip
