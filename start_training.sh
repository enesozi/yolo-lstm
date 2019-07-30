cd "$PWD/darknet/build/darknet/x64/"
../../../darknet detector train data/lstm.data yolo_v3_spp_lstm.cfg darknet53.conv.74 -gpus 3 -dont_show  -map >> /home/Downloads/tra_results.txt
