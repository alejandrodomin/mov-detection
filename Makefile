demo-live:
	python src/main.py --live --frame_rate 60

demo-fish:
	python src/main.py --input_file ./data/video/fish.mp4

demo-balloons:
	python src/main.py --input_file ./data/video/balloons.mp4

debug:
	python -m pdb src/main.py --input_file ./data/video/balloons.mp4
