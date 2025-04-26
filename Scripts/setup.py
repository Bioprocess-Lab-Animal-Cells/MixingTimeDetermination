""" MIXING TIME DETERMINATION - Using Colorimetric Method
By Yago Silva, Fernando Cecatto and Elisabeth Augusto
Bioprocess Laboratory with Animal Cells - Science and Technology Institute, Federal University of São Paulo
Definition of the pixel areas on the video """

import cv2


coordinates = []


def area_selection(img):
	""" Selection of the 4 areas """
	with open('info_msg.ini', 'a') as doc:
		doc.writelines(" OK\nSelect four areas ... ")

	image = cv2.imread(img)

	result = []
	rois = []
	roi_count = 0
	while roi_count < 4:
		choice = cv2.selectROI("Select four areas (Press Space to confirm the selection):", image)
		rois.append(list(choice))
		roi_count += 1

	cv2.destroyAllWindows()
	
	for i in rois:
		pixels = [i[0], i[1], i[0] + i[2], i[1] + i[3]]
		pixels = str(pixels)
		result.append(pixels + "\n")

	file = open("cartesian.ini", "w")
	file.writelines(result)


def reading_areas():
	""" Read the areas coordinates """
	file = open("./Scripts/cartesian.ini")
	positions = file.readlines()
	num = ''
	global coordinates

	for row in positions:
		for i in row:
			if i != "," and i != "]":
				if i.isdigit():
					num += i
			else:
				coordinates.append(int(num))
				num = ''


def select_option(img, answer):
	""" User option to select the areas or not """
	if answer == 1:
		area_selection(img)
