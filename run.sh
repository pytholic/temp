#!/bin/bash

#read -p 'Enter your project path ' project_path

# Copy video to server
if [[ $1 =~ ^(-p|--project_path) ]]
then
    project_path="$2"
fi
echo "Project path is $project_path"
echo "Copying file..."
scp -r ./tmp pytholic@10.160.50.25:"$project_path/"
echo "Copy process finished..."


# Extracting frames and running droid-slam
if [[ $3 =~ ^(-s|--server_ip) ]]
then
    server_ip="$4"
fi

env="$6"
cam="$8"

ssh "$server_ip" ". ~/.zshrc; cd "$project_path"; conda activate droidenv; echo "Starting frame extraction..."; python3 ./utils/extract_frames_ffmpeg.py -d $cam; echo "Frame extraction completed...";
mkdir $project_path/tmp/output; echo "Running droid-slam..."; python3 demo.py --imagedir=$project_path/tmp/frames --calib=./calib/$cam.txt --reconstruction_path=$project_path/tmp/output; echo "Droid-slam completed...""

# Fetch results
mkdir ./results
scp "pytholic@$server_ip:$project_path/tmp/output/*" ./results

# Remove tmp folder from server
ssh "$server_ip" rm -r $project_path/tmp

# Visualize and remove outlier
conda activate open3d
python3 vis.py; python3 outlier_removal.py





