""" MIXING TIME DETERMINATION - Using Colorimetric Method
By Yago Silva, Fernando Cecatto and Elisabeth Augusto
Bioprocess Laboratory with Animal Cells - Science and Technology Institute, Federal University of São Paulo
This code is the main part to determine the mixing time """
import cv2
import PIL.Image
import os
import shutil
import matplotlib.pyplot as plt
import concurrent.futures
import math
from time import sleep
import setup
import numpy as np
import xlsxwriter


def create_folder(folder):

    """ Create a new folder for the frames. If it exists will be deleted and created a new one. """

    # folder = input("Digite o name da nova folder do experimento: ")

    # Criacao da folder com os frames
    if os.path.exists(folder):
        shutil.rmtree(folder)

    os.makedirs(folder)


def generate_frames(vid, folder):

    """ Converts the video into frames image """

    video = cv2.VideoCapture(vid)

    currentframe = 0
    names_list = []

    while True:

        ret, frame = video.read()

        if ret:
            name = "".join([f'./{folder}/frame{str(currentframe)}.jpg'])
            names_list.append(name)
            print("".join(['Creating...', name]))

            cv2.imwrite(name, frame)

            currentframe += 1

        else:
            break

    return currentframe, video, names_list


def top_pixels(l_names):
    """ Returns the green of the pixels of the first frame """

    result = []

    im = PIL.Image.open(l_names[1])
    image = im.convert("RGB")
    setup.reading_areas()
    coordinates = setup.coordinates

    area1 = [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]
    area2 = [coordinates[4], coordinates[5], coordinates[6], coordinates[7]]
    area3 = [coordinates[8], coordinates[9], coordinates[10], coordinates[11]]
    area4 = [coordinates[12], coordinates[13], coordinates[14], coordinates[15]]
    areas = [area1, area2, area3, area4]

    for area in areas:

        for row in range(area[0], area[2]):
            for col in range(area[1], area[3]):
                red, green, blue = image.getpixel((row, col))
                result.append(green)
    global initial_frame
    initial_frame = result


def std_pixels(img):
    """ Returns the saturation of the tracer injection area of the frame to find the initial frame of the experiment """
    setup.reading_areas()
    coordinates = setup.coordinates
    area1 = [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]
    im = cv2.imread(img)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    sat_vet = []

    for row in range(area1[0], area1[2]):
        for col in range(area1[1], area1[3]):
            hue, saturation, value = image[col, row]
            sat_vet.append(np.float64(saturation))
    samp_sd = np.std(sat_vet, ddof=1)
    return samp_sd


def start_frame(samp_sd):
    """ Determines the frame that the experiment started. """

    count = 1

    diff_vet = []

    while count < len(samp_sd):
        diff = (samp_sd[count] - samp_sd[count - 1]) * 100 / samp_sd[count - 1]
        diff_vet.append(diff)
        count += 1

    return diff_vet


def return_frame0(diff_vet, folder):
    """ Returns the experiment initial frame"""
    f0 = max(diff_vet)
    for i in range(len(diff_vet)):
        if f0 == diff_vet[i]:
            framevalue = i + 1
            break

    frame0 = f"./{folder}/frame{framevalue}.jpg"

    return frame0, framevalue


def last_pixels(frame):
    """ Creates a matrix of the last 150 frames. """
    im = PIL.Image.open(frame)
    image = im.convert("RGB")
    setup.reading_areas()
    coordinates = setup.coordinates
    matrix = []

    area1 = [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]
    area2 = [coordinates[4], coordinates[5], coordinates[6], coordinates[7]]
    area3 = [coordinates[8], coordinates[9], coordinates[10], coordinates[11]]
    area4 = [coordinates[12], coordinates[13], coordinates[14], coordinates[15]]
    areas = [area1, area2, area3, area4]

    for area in areas:

        for row in range(area[0], area[2]):
            for col in range(area[1], area[3]):
                red, green, blue = image.getpixel((row, col))
                matrix.append(green)

    return matrix


def final_pixel(matrix):
    """ Constructs the last frame, an average of the last 150 frames. It is used to normalize the results. """
    result = []
    for pixel in range(len(matrix[0])):
        pixel_sum = 0
        for frame in matrix:
            pixel_sum += frame[pixel]
        mean_pixel = pixel_sum/len(matrix)
        result.append(mean_pixel)
    global last_frame
    last_frame = result


def global_parameters(l_names, matrix):
    """ Global parameters to multiprocessing functions. """
    top_pixels(l_names)
    final_pixel(matrix)


def analyze_means_rgb(img):
    """ Color change analysis - Mean green method """
    im = cv2.imread(img)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    
    setup.reading_areas()
    coordinates = setup.coordinates

    area1 = [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]
    area2 = [coordinates[4], coordinates[5], coordinates[6], coordinates[7]]
    area3 = [coordinates[8], coordinates[9], coordinates[10], coordinates[11]]
    area4 = [coordinates[12], coordinates[13], coordinates[14], coordinates[15]]
    areas = [area1, area2, area3, area4]

    result = []

    for area in areas:

        subtotal_rgb, num_pixels = 0, 0
        for row in range(area[0], area[2]):
            for col in range(area[1], area[3]):
                red, green, blue = image[col, row]
                subtotal_rgb += np.float64(green)
                num_pixels += 1

        if area == area1:
            result.append([subtotal_rgb, num_pixels])

        elif area == area2:
            result.append([subtotal_rgb, num_pixels])

        elif area == area3:
            result.append([subtotal_rgb, num_pixels])

        elif area == area4:
            result.append([subtotal_rgb, num_pixels])

    return result


def analyze_samp_sd_rgb(img):
    """ Color change analysis - standard deviation and M methods """
    i_frame = initial_frame
    l_frame = last_frame
    pixelsa1, pixelsa2, pixelsa3, pixelsa4 = [], [], [], []
    n_mix_a1, n_mix_a2, n_mix_a3, n_mix_a4 = 0, 0, 0, 0
    total_n_a1, total_n_a2, total_n_a3, total_n_a4 = 0, 0, 0, 0
    x = 0.40
    im = cv2.imread(img)
    image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
 
    setup.reading_areas()
    coordinates = setup.coordinates

    area1 = [coordinates[0], coordinates[1], coordinates[2], coordinates[3]]
    area2 = [coordinates[4], coordinates[5], coordinates[6], coordinates[7]]
    area3 = [coordinates[8], coordinates[9], coordinates[10], coordinates[11]]
    area4 = [coordinates[12], coordinates[13], coordinates[14], coordinates[15]]
    areas = [area1, area2, area3, area4]

    count = 0

    for area in areas:
        for row in range(area[0], area[2]):
            for col in range(area[1], area[3]):
                red, green, blue = image[col, row]
                pixel = (np.float64(green) - np.float64(i_frame[count]))/(np.float64(l_frame[count]) -
                                                                          np.float64(i_frame[count]))

                if area == area1:
                    pixelsa1.append(pixel)
                    total_n_a1 += 1
                    if pixel > x:
                        n_mix_a1 += 1

                elif area == area2:
                    pixelsa2.append(pixel)
                    total_n_a2 += 1
                    if pixel > x:
                        n_mix_a2 += 1

                elif area == area3:
                    pixelsa3.append(pixel)
                    total_n_a3 += 1
                    if pixel > x:
                        n_mix_a3 += 1

                elif area == area4:
                    pixelsa4.append(pixel)
                    total_n_a4 += 1
                    if pixel > x:
                        n_mix_a4 += 1
                count += 1
# SD method
    stdeva1 = np.std(pixelsa1, ddof=1)
    stdeva2 = np.std(pixelsa2, ddof=1)
    stdeva3 = np.std(pixelsa3, ddof=1)
    stdeva4 = np.std(pixelsa4, ddof=1)
    stdev_image = np.std(pixelsa1 + pixelsa2 + pixelsa3 + pixelsa4, ddof=1)
# M method
    m_a1 = n_mix_a1/total_n_a1
    m_a2 = n_mix_a2/total_n_a2
    m_a3 = n_mix_a3/total_n_a3
    m_a4 = n_mix_a4/total_n_a4
    m = (n_mix_a1 + n_mix_a2 + n_mix_a3 + n_mix_a4)/(total_n_a1 + total_n_a2 + total_n_a3 + total_n_a4)

    result = [stdeva1, stdeva2, stdeva3, stdeva4, stdev_image, m_a1, m_a2, m_a3, m_a4, m]

    return result


def refresh_info_msg(text):
    """ Refresh the program step for the GUI """
    with open('info_msg.ini', 'a') as doc:
        doc.writelines(text)


def main():
    # User data in the GUI
    vid = ""
    folder = ""
    time_cut = 0
    name = ""
    selection = 0
    count = 0
    with open("data_info.ini", "r") as file:
        data = file.readlines()
    for i in range(5):
        word = ""
        while data[0][count] != "§":
            word += data[0][count]
            count += 1
        if i == 0:
            vid = word
        elif i == 1:
            folder = word
        elif i == 2:
            time_cut = int(word)
        elif i == 3:
            selection = int(word)
        else:
            name = word
        count += 1

    create_folder(folder)  # Creates a folder to the frames

    text = "Creating and saving frames ... "
    refresh_info_msg(text)

    currentframe, video, l_names = generate_frames(vid, folder)  # Generates the frames and saves in the folder

    setup.select_option(l_names[0], selection)  # Selection of the areas

    fps = float(video.get(cv2.CAP_PROP_FPS))
    frame_range = 3*(video.get(cv2.CAP_PROP_FRAME_COUNT))//5
    first_frames = l_names.copy()
    del first_frames[-round(currentframe - frame_range):]

    text = " OK\nSearching the initial frame of the experiment ... "
    refresh_info_msg(text)
    print("Searching the initial frame of the experiment...")

    # Determination of the initial frame
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future = executor.map(std_pixels, first_frames)
        samp_sd = list(future)

    diff_vet = start_frame(samp_sd)
    frame0, frame_number = return_frame0(diff_vet, folder)

    text = f" OK\nInitial frame: {frame_number}"
    refresh_info_msg(text)
    print(f'Initial frame: {frame_number}')

    start = 0
    for i in range(len(l_names)):
        if l_names[i] == frame0:
            start = i

    names_list = l_names[start:len(l_names)]
    currentframe -= start

    # Removes the final frames from the analysis
    if time_cut != 0:
        frame_cut = math.floor(time_cut * fps)

        currentframe -= frame_cut

        del names_list[-frame_cut:]

    text = "\nCalculating the average of the last 150 frames ... "
    refresh_info_msg(text)
    print('Calculating the average of the last 150 frames...')

    # Creation of the last frame, an average of the last 150 frames
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_rgb = executor.map(last_pixels, names_list[-150:])
        final_pixels = list(future_rgb)

    # Variables declaration

    means_rgb_a1, means_rgb_a2, means_rgb_a3, means_rgb_a4, means_rgb = [], [], [], [], []
    stddev_rgb_a1, stddev_rgb_a2, stddev_rgb_a3, stddev_rgb_a4, stddev_rgb = [], [], [], [], []
    m_a1, m_a2, m_a3, m_a4, m = [], [], [], [], []
    means_normal_rgb = []
    vector_time = []

    text = " OK\nCalculating mean values ... "
    refresh_info_msg(text)
    print('Calculating mean values...')

    # Mean green method
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_rgb = executor.map(analyze_means_rgb, names_list)
        result_rgb = list(future_rgb)

    num_pixels_a1 = result_rgb[0][0][1]
    num_pixels_a2 = result_rgb[0][1][1]
    num_pixels_a3 = result_rgb[0][2][1]
    num_pixels_a4 = result_rgb[0][3][1]
    total_pixels = num_pixels_a1 + num_pixels_a2 + num_pixels_a3 + num_pixels_a4

    for i in result_rgb:
        mean_rgb_a1 = i[0][0] / num_pixels_a1
        means_rgb_a1.append(mean_rgb_a1)
        mean_rgb_a2 = i[1][0] / num_pixels_a2
        means_rgb_a2.append(mean_rgb_a2)
        mean_rgb_a3 = i[2][0] / num_pixels_a3
        means_rgb_a3.append(mean_rgb_a3)
        mean_rgb_a4 = i[3][0] / num_pixels_a4
        means_rgb_a4.append(mean_rgb_a4)
        means_rgb.append((i[0][0] + i[1][0] + i[2][0] + i[3][0]) / total_pixels)

    text = " OK\nCalculating SD and M (Cabaret) values ... "
    refresh_info_msg(text)
    print('Calculating SD and M values...')

    # SD and M methods
    with (concurrent.futures.ProcessPoolExecutor(initializer=global_parameters, initargs=(l_names, final_pixels))
          as executor):
        future_rgb = executor.map(analyze_samp_sd_rgb, names_list)
        result_rgb = list(future_rgb)

    for i in result_rgb:
        stddev_rgb_a1.append(i[0])
        stddev_rgb_a2.append(i[1])
        stddev_rgb_a3.append(i[2])
        stddev_rgb_a4.append(i[3])
        stddev_rgb.append(i[4])
        m_a1.append(i[5])
        m_a2.append(i[6])
        m_a3.append(i[7])
        m_a4.append(i[8])
        m.append(i[9])

    # Normalizing the mean green

    final_pixel(final_pixels)

    final_mean_rgb = np.mean(means_rgb[-150:])
    stddev = np.std(means_rgb[-150:], ddof=1)
    vc = stddev/final_mean_rgb*100

    text = " OK\nNormalizing mean values ... "
    refresh_info_msg(text)
    print('Normalizing mean values...')
    for value in range(len(means_rgb)):
        normal_rgb = abs((means_rgb[value]-means_rgb[0])/(final_mean_rgb-means_rgb[0]))
        means_normal_rgb.append(normal_rgb)

    # Creation of the time vector
    vector_frames = list(range(currentframe))

    for value in vector_frames:
        time = value/fps
        vector_time.append(time)

    # Determination of the mixing time

    mixing = False
    count = 0
    while not mixing:
        if means_normal_rgb[count] >= 0.95:
            mixtime_rgb_mean = vector_time[count]
            mixing = True
        count += 1

    last_std = np.mean(stddev_rgb[-150:])
    last_std += 0.05*last_std
    mixing = False
    count = 0
    while not mixing:
        if stddev_rgb[count] < last_std:
            mixtime_rgb_std = vector_time[count]
            mixing = True
        count += 1

    mixing = False
    count = 0
    while not mixing:
        if m[count] >= 0.95:
            mixtime_rgb_m = vector_time[count]
            mixing = True
        count += 1

    # Generation of the graphs and the worksheet
    sheet = f'{name}.xlsx'
    workbook = xlsxwriter.Workbook(sheet)
    worksheet = workbook.add_worksheet()

    title = ['Time (s)', 'MeanA1', 'MeanA2', 'MeanA3', 'MeanA4', 'Mean', 'Normalized Mean', 'Std.Dev.A1',
             'Std.Dev.A2', 'Std.Dev.A3', 'Std.Dev.A4', 'Std.Dev.', 'M_A1', 'M_A2', 'M_A3', 'M_A4', 'M',
             'Mixing Time (s)']
    for i in range(len(title)):
        worksheet.write(0, i, title[i])

    col = 0
    for row in range(1, len(means_rgb_a1)):
        worksheet.write(row, col, vector_time[row - 1])
        col += 1
        worksheet.write(row, col, means_rgb_a1[row - 1])
        col += 1
        worksheet.write(row, col, means_rgb_a2[row - 1])
        col += 1
        worksheet.write(row, col, means_rgb_a3[row - 1])
        col += 1
        worksheet.write(row, col, means_rgb_a4[row - 1])
        col += 1
        worksheet.write(row, col, means_rgb[row - 1])
        col += 1
        worksheet.write(row, col, means_normal_rgb[row - 1])
        col += 1
        worksheet.write(row, col, stddev_rgb_a1[row - 1])
        col += 1
        worksheet.write(row, col, stddev_rgb_a2[row - 1])
        col += 1
        worksheet.write(row, col, stddev_rgb_a3[row - 1])
        col += 1
        worksheet.write(row, col, stddev_rgb_a4[row - 1])
        col += 1
        worksheet.write(row, col, stddev_rgb[row - 1])
        col += 1
        worksheet.write(row, col, m_a1[row - 1])
        col += 1
        worksheet.write(row, col, m_a2[row - 1])
        col += 1
        worksheet.write(row, col, m_a3[row - 1])
        col += 1
        worksheet.write(row, col, m_a4[row - 1])
        col += 1
        worksheet.write(row, col, m[row - 1])
        col = 0

    worksheet.write(1, 17, 'Mean:')
    worksheet.write(1, 18, mixtime_rgb_mean)
    worksheet.write(2, 17, 'Std. Dev.:')
    worksheet.write(2, 18, mixtime_rgb_std)
    worksheet.write(3, 17, 'Cabaret M:')
    worksheet.write(3, 18, mixtime_rgb_m)
    workbook.close()
    text = " OK\nGenerating graphs ... "
    refresh_info_msg(text)
    print('Generating graphs...')
    sleep(1)

    text = (" OK\n\nMixing time (s): \n" + f"Mean: {mixtime_rgb_mean:.2f}\n" +
            f"Standard Deviation: {mixtime_rgb_std:.2f}\n" + f"Cabaret M: {mixtime_rgb_m:.2f}\n")
    refresh_info_msg(text)
    print(f"Mixing Time (Mean): {mixtime_rgb_mean:.2f} s")
    print(f"Mixing Time (SD): {mixtime_rgb_std:.2f} s")
    print(f"Mixing Time (Cabaret): {mixtime_rgb_m:.2f} s")

    fig, axs = plt.subplots(2, 3)
    # Mean green per area
    axs[0, 0].plot(vector_time, means_rgb_a1, color='blue', label='Area 1')
    axs[0, 0].plot(vector_time, means_rgb_a2, color='green', label='Area 2')
    axs[0, 0].plot(vector_time, means_rgb_a3, color='red', label='Area 3')
    axs[0, 0].plot(vector_time, means_rgb_a4, color='yellow', label='Area 4')
    axs[0, 0].set_title("Means Green")
    axs[0, 0].legend()

    # Normalized mean green method
    axs[1, 0].plot(vector_time, means_normal_rgb, color='black')
    axs[1, 0].set_title('Normalized Mean Green')
    axs[1, 0].fill_between(vector_time, 0.95, 1.05, color='grey', alpha=.3)
    axs[1, 0].axvline(x=mixtime_rgb_mean, linestyle="dashed", ymax=0.95, color='red')
    axs[1, 0].sharex(axs[0, 0])
    axs[1, 0].set_xlabel('Time (s)')

    # SD green per area
    axs[0, 1].plot(vector_time, stddev_rgb_a1, color='blue', label='Area 1')
    axs[0, 1].plot(vector_time, stddev_rgb_a2, color='green', label='Area 2')
    axs[0, 1].plot(vector_time, stddev_rgb_a3, color='red', label='Area 3')
    axs[0, 1].plot(vector_time, stddev_rgb_a4, color='yellow', label='Area 4')
    axs[0, 1].set_title("SD Green")
    axs[0, 1].legend()

    # Normalized SD green
    axs[1, 1].plot(vector_time, stddev_rgb, color='black')
    axs[1, 1].set_title('Total SD Green')
    axs[1, 1].fill_between(vector_time, 0.95*last_std, 1.05*last_std, color='grey', alpha=.3)
    axs[1, 1].axvline(x=mixtime_rgb_std, linestyle="dashed", ymax=0.05, color='red')
    axs[1, 1].sharex(axs[0, 1])
    axs[1, 1].set_xlabel('Time (s)')

    # M green per area
    axs[0, 2].plot(vector_time, m_a1, color='blue', label='Area 1')
    axs[0, 2].plot(vector_time, m_a2, color='green', label='Area 2')
    axs[0, 2].plot(vector_time, m_a3, color='red', label='Area 3')
    axs[0, 2].plot(vector_time, m_a4, color='yellow', label='Area 4')
    axs[0, 2].set_title("M (Cabaret et al., 2007)")
    axs[0, 2].legend()

    # M green method
    axs[1, 2].plot(vector_time, m, color='black')
    axs[1, 2].set_title('Total M')
    axs[1, 2].fill_between(vector_time, 0.95, 1.05, color='grey', alpha=.3)
    axs[1, 2].axvline(x=mixtime_rgb_m, linestyle="dashed", ymax=0.95, color='red')
    axs[1, 2].sharex(axs[0, 2])
    axs[1, 2].set_xlabel('Time (s)')

    plt.show()

    text = "\nFINISHED!"
    refresh_info_msg(text)
    print('FINISHED!')

    # Finishes the program
    video.release()
    cv2.destroyAllWindows()


initial_frame = []
last_frame = []
if __name__ == '__main__':
    main()
