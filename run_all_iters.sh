for iter in {17000..1000..1000}
do
	../../../darknet detector map data/lstm.data yolo_v3_spp_lstm.cfg backup/yolo_v3_spp_lstm${iter}.weights -gpus 3 >> val_res.txt 
done
