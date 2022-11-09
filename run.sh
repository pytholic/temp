#!/bin/bash

#read -p 'Enter your project path ' project_path

# Copy video to server
if [[ $1 =~ ^(-p|--project_path) ]]
then
    project_path="$2"
fi
echo "Project path is $project_path"
echo "Copying file..."
#scp -r ./tmp pytholic@10.160.50.25:"$project_path/"
echo "Copy process finished..."


# Extracting frames and running droid-slam
if [[ $3 =~ ^(-s|--server_ip) ]]
then
    server_ip="$4"
fi

env="$6"
cam="$8"

#echo "Starting frame extraction..."
ssh "$server_ip" ". ~/.zshrc; cd "$project_path"; conda activate droidenv; python3 ./utils/extract_frames.py -c $cam; echo "Frame extraction completed...";
echo "Running droid-slam..."; python3 demo.py --imagedir=$project_path/tmp/frames --calib=./calib/gopro.txt --reconstruction_path=$project_path/tmp/output" 

# ssh "$server_ip" ". ~/.zshrc; cd "$project_path"; conda activate droidenv; mkdir -p ./tmp/output; echo "Starting frame extraction...";
# python3 ./utils/extract_frames.py; echo "Frame extraction completed...";" 

# ssh "$server_ip" ". ~/.zshrc; cd "$project_path"; conda activate droidenv; echo "Running droid-slam..."; 
# python3 demo.py --imagedir=$project_path/tmp/frames --calib=./calib/gopro.txt --reconstruction_path=$project_path/tmp/output" 

