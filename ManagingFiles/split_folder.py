import glob
import random
import os
import shutil
image_exts = ['.jpg', '.png', '.jpeg']


def split_folder_into_train_val_test(ann_folder, image_folder, output_folder, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Splits a folder into train, val, and test subdirectories.

    Arguments:
    folder_path -- the path to the folder to split
    output_folder -- the path to the output folder where the train, val, (test) subdirectories will be created
    train_ratio -- the ratio of files to include in the train subdirectory (default 0.8)
    val_ratio -- the ratio of files to include in the validation subdirectory (default 0.1)
    test_ratio -- the ratio of files to include in the test subdirectory (default 0.1)
    """
    # create output folders
    train_folder, val_folder, test_folder = create_model_train_folder_structure(output_folder)
    # get list of files
    files =  glob_text_files(ann_folder)
    filenames = []
    for filename in files:
        if filename == 'classes.txt':
            continue
        else:
            filenames.append(os.path.basename(filename)[:-4]) # remove the extension

    # shuffle the files
    random.shuffle(filenames)

    #splitting our data into with the given ratios..
    train_files, val_files, test_files = get_train_val_test_split_ratio(filenames, train_ratio, val_ratio)

    # move files to output folders
    for file_list, folder_name in [(train_files, train_folder), (val_files, val_folder), (test_files, test_folder)]:
        for file in file_list:
            # move label file
            label_file = file + '.txt'
            src_path = os.path.join(ann_folder, label_file)
            dst_path = os.path.join(folder_name, 'labels', label_file)
            shutil.move(src_path, dst_path)

            # move image file
            for ext in image_exts:
                image_file = file + ext
                src_path = os.path.join(image_folder, image_file)
                if os.path.exists(src_path):
                    dst_path = os.path.join(folder_name, 'images', image_file)
                    shutil.move(src_path, dst_path)
                    break  # break out of loop once the image is found and moved

    return train_folder, val_folder, test_folder

#utils


def create_model_train_folder_structure(output_folder):
    train_folder = os.path.join(output_folder, 'train')
    val_folder = os.path.join(output_folder, 'val')
    test_folder = os.path.join(output_folder, 'test')
    for folder in [train_folder, val_folder, test_folder]:
        os.makedirs(os.path.join(folder, 'images'))
        os.makedirs(os.path.join(folder, 'labels'))
    return train_folder, val_folder, test_folder


def glob_text_files(ann_folder, ext='.txt'):
    return glob.glob(os.path.join(ann_folder, '*' + ext))


def get_train_val_test_split_ratio(data, train_ratio, val_ratio):
    num_files = len(data)
    num_train = int(train_ratio * num_files)
    num_val = int(val_ratio * num_files)

    train_data= data[:num_train]
    val_data = data[num_train:num_train + num_val]
    test_data = data[num_train + num_val:]

    return train_data, val_data, test_data