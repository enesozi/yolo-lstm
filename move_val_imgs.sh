    while IFS= read line
	do
		cp  "${line}" "$HOME/Downloads/val_all" 2>/dev/null
	done <"lstm_valid.txt"

