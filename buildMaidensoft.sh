#!/bin/bash

#TO-DO
#1. Compile with NSIS
#2. upload to GDrive
#3. output the shareable URL
#4. option for launching the app


PROJECT_DIR=$1;
OUTPUT_DIR=$2;

cd $PROJECT_DIR;

mvn package &&

[ ! -d "$OUTPUT_DIR" ] && mkdir -p "$OUTPUT_DIR";

mkdir -p $OUTPUT_DIR/reports && 
cp -avrf $PROJECT_DIR/reports/*.jasper $OUTPUT_DIR/reports &&
cp -avrf $PROJECT_DIR/target/lib $OUTPUT_DIR &&
cp -avf $PROJECT_DIR/target/Maidensoft*.jar $OUTPUT_DIR/Maidensoft.jar &&
cp -avrf $PROJECT_DIR/data $OUTPUT_DIR;

echo "Done.";
