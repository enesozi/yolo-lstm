cd "$PWD/darknet/build/darknet/x64/"
../../../darknet detector train data/lstm.data yolov3-fine.cfg yolov3_fine.conv.81 -gpus 2 -dont_show  -map -clear >> /home/Downloads/tra_results.txt
