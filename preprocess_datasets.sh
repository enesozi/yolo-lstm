#!/bin/bash
declare -a train_images=("winter" "thermal" "demo")
declare -a valid_images=("rescue")
train_file="lstm_train.txt"
valid_file="lstm_valid.txt"
cfg_file="yolo_v3_spp_lstm.cfg"
data_file="lstm.data"
name_file="lstm.names"
image_dir="$PWD/darknet/build/darknet/x64/data/lstm"

[ -f "$train_file" ] && rm "$train_file"
[ -f "$valid_file" ] && rm "$valid_file"

rm -rf "$image_dir"
mkdir "$image_dir"

for ds in $train_images
do
echo $ds
python xml2json.py ${ds} "$HOME/Downloads/${ds}_xml"  "$HOME/Downloads/${ds}"
python convert_coco_yolo.py "${ds}.json" "${ds}" "${image_dir}"
end=$(cat "${ds}.txt")
        for value in $( eval echo {0..$end} )
        do
                printf "data/lstm/${ds}_frame%05d.jpg\n" $value >> "$train_file";
                image=$(printf "frame%05d.jpg" $value)
                # Copy image to the correct directory
                cp "$HOME/Downloads/${ds}/${image}" "${image_dir}/${ds}_${image}" 2>/dev/null
        done

done

for ds in $valid_images
do
echo $ds
python xml2json.py ${ds} "$HOME/Downloads/${ds}_xml"  "$HOME/Downloads/${ds}"
python convert_coco_yolo.py "${ds}.json" "${ds}" "${image_dir}"
end=$(cat "${ds}.txt")
        for value in $( eval echo {0..$end} )
        do
                printf "data/lstm/${ds}_frame%04d.jpg\n" $value >> "$valid_file";
                image=$(printf "frame%05d.jpg" $value)
                # Copy image to the correct directory
                cp "$HOME/Downloads/${ds}/${image}" "${image_dir}/${ds}_${image}" 2>/dev/null
        done

done

# Copy necessary files to the correct directories
cp "$cfg_file"   "$PWD/darknet/build/darknet/x64/"
cp "$train_file" "$PWD/darknet/build/darknet/x64/data/"
cp "$valid_file" "$PWD/darknet/build/darknet/x64/data/"
cp "$data_file"  "$PWD/darknet/build/darknet/x64/data/"
cp "$name_file"  "$PWD/darknet/build/darknet/x64/data/"
cp "run_all_iters.sh" "$PWD/darknet/build/darknet/x64/"

# Download pretrained weight
wget https://pjreddie.com/media/files/darknet53.conv.74 -O "$PWD/darknet/build/darknet/x64/darknet53.conv.74"
