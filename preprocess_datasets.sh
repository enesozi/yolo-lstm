#!/bin/bash
declare -a train_images=("thermal" "winter" "rescue895" "rescue896")
declare -a valid_images=("thermal" "winter" "rescue895" "rescue896")
declare -A train_limits=( ["thermal"]=3800 ["winter"]=4701 ["rescue895"]=150 ["rescue896"]=-1)

train_file="lstm_train.txt"
valid_file="lstm_valid.txt"
cfg_file="yolov3-spp-fine.cfg"
data_file="lstm.data"
name_file="lstm.names"
#image_dir="$PWD/darknet/build/darknet/x64/data/lstm"
image_dir="$HOME/Downloads/lstm"

[ -f "$train_file" ] && rm "$train_file"
[ -f "$valid_file" ] && rm "$valid_file"

rm -rf "$image_dir"
mkdir "$image_dir"

for ds in "${train_images[@]}";
do
echo $ds
python xml2json.py ${ds} "$HOME/Downloads/${ds}_xml"  "$HOME/Downloads/${ds}"
python convert_coco_yolo.py "${ds}.json" "${ds}" "${image_dir}"
i=0
	while IFS= read line
	do
		printf "$HOME/Downloads/lstm/${ds}_$line\n" >> "$train_file";
		cp "$HOME/Downloads/${ds}/${line}" "${image_dir}/${ds}_${line}" 2>/dev/null
		i=$(($i + 1))
		if [ $i -eq "${train_limits[$ds]}" ]
		then 
			break
		fi
	done <"${ds}.txt"
done

for ds in "${valid_images[@]}";
do
echo $ds
i=0
	while IFS= read line
	do
		if [ $i -gt "${train_limits[$ds]}" ]
		then
			printf "$HOME/Downloads/lstm/${ds}_$line\n" >> "$valid_file";
			cp "$HOME/Downloads/${ds}/${line}" "${image_dir}/${ds}_${line}" 2>/dev/null
		fi
		i=$(($i + 1))
	done <"${ds}.txt"

done

shuf "$train_file" > "train_file_shuffled.txt"
mv "train_file_shuffled.txt" "$train_file"

shuf "$valid_file" > "valid_file_shuffled.txt"
mv "valid_file_shuffled.txt" "$valid_file"

# Copy necessary files to the correct directories
#cp "$cfg_file"   "$PWD/darknet/build/darknet/x64/"
cp "$train_file" "$PWD/darknet/build/darknet/x64/data/"
cp "$valid_file" "$PWD/darknet/build/darknet/x64/data/"
#cp "$data_file"  "$PWD/darknet/build/darknet/x64/data/"
#cp "$name_file"  "$PWD/darknet/build/darknet/x64/data/"
#cp "run_all_iters.sh" "$PWD/darknet/build/darknet/x64/"

# Download pretrained weight
#wget https://pjreddie.com/media/files/darknet53.conv.74 -O "$PWD/darknet/build/darknet/x64/darknet53.conv.74"



