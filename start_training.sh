cd "$PWD/darknet/build/darknet/x64/"
../../../darknet detector train data/lstm.data yolo_v3_spp_lstm.cfg yolov3-spp.conv.85 -gpus 2 -dont_show  -map >> /home/Downloads/tra_results.txt
