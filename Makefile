demo-live:
	python main.py --live --frame_rate 60

demo-fish:
	python main.py --input_file ./video/fish.mp4

demo-balloons:
	python main.py --input_file ./vide/balloons.mp4  

debug:
	python -m pdb main.py --input_file ./video/balloons.mp4
