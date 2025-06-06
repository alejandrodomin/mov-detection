from python import Python

def main():
	var cv2 = Python.import_module("cv2")
	capture = cv2.VideoCapture(0)

	while capture.isOpened():
		var cap = capture.read()
		var ret = cap[0]
		var frame = cap[1]
        
		if ret:
			cv2.namedWindow('Boxed', cv2.WINDOW_NORMAL)
			cv2.imshow('Boxed', frame)

	capture.release()
	cv2.destroyAllWindows()
