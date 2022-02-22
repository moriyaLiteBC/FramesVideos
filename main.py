import sys
import os
import cv2
import csv

frames_per_second = 0.00234192037470726


def program(root_path, writer_file):
    global frames_per_second

    root_directory = os.fsencode(root_path)
    total_movies = 0
    for patient_file in os.listdir(root_directory):
        name_patient = patient_file.decode("utf-8")
        patient_data = [name_patient]
        counter_scans_dir =0
        counter_movies = 0
        patient_directory =os.fsdecode(os.path.join(root_directory, patient_file))
        for data_dirs in os.listdir(patient_directory):
            if data_dirs.startswith("scan"):
                counter_scans_dir +=1
                scan_directory = os.fsdecode(os.path.join(patient_directory, data_dirs))
                for scan_file in os.listdir(scan_directory):  # go throth over all movies folders and scans
                    movie_directory = os.fsdecode(os.path.join(scan_directory, scan_file))
                    if os.path.isdir(movie_directory):
                        counter_movies += 1
                        total_movies +=1
                        for file in os.listdir(movie_directory):
                            if file == "Bright.avi":
                                frames = count_frames(os.path.join(movie_directory, file))
                                patient_data.append(frames*frames_per_second)
        writer_file.writerow(patient_data)
        print(name_patient  + ": scan_dirs: " + str(counter_scans_dir) + " movies: " +str(counter_movies))
    print("total moves: " + str(total_movies))


def count_frames(path_file):
    try:
        video = cv2.VideoCapture(path_file)
        if not video.isOpened():
            return 0
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        return length
    except cv2.error as e:
        return 0


def create_excel_file(target):
    result_file = open(target, 'w')
    writer_f = csv.writer(result_file)
    header = ["name"]
    for i in range(10):
        s = "movie" + str(i+1)
        header.append(s)
    writer_f.writerow(header)
    return writer_f


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception("Enter a path to the program")

    result_path = os.path.join(sys.argv[2], "results.csv")
    writer = create_excel_file(result_path)
    root_path = sys.argv[1]
    program(root_path, writer)