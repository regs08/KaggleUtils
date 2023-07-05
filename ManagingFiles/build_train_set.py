import os
import shutil
import re
from KaggleUtils.ManagingFiles.split_folder import split_folder_into_train_val_test
from KaggleUtils.ManagingFiles.write_yaml import write_data_yaml_file
import random

IMAGE_EXTS=(".jpg", ".jpeg", ".png")
"""
  here we build our trainset. we iterate through the list of train folders -label
  name with two sub folders, images and labels- to move the files to a folder
  then they will be split into train val and test sets. images and anns will be
  copied to the out folders provided in the constructor
"""


class TrainSetBuilder:
    def __init__(self, train_folders, out_folder, single_class=None, split_folder=None, seed=42):
        self.train_folders = train_folders
        self.out_folder = out_folder
        self.single_class = single_class
        self.split_folder = split_folder

        self.image_out_folder = os.path.join(out_folder, 'images')
        self.ann_out_folder = os.path.join(out_folder, 'labels')
        self.label_path_map = self.get_label_path_map(train_folders)

        self.label_id_map = self.build_label_id_map()
        self.id_label_map = {value: key for key, value in self.label_id_map.items()}
        self.class_labels = list(self.label_id_map.keys())
        random.seed(seed)

    def build_train_set(self, subset=None):
        """
        iterates through our data and copies images and labels into a folder where they can besplit into a train-set
        :param subset: toggle if you just want
        :return:
        """
        keys = list(self.label_id_map.keys())
        for folder in self.label_path_map:
            #print(f"Copying {folder} ann files to {self.ann_out_folder}...")
            labels_folder = os.path.join(self.label_path_map[folder], "labels")
            images_folder = os.path.join(self.label_path_map[folder], "images")

            #gets image and label paths, toggle subset param for random subset from each folder
            image_file_paths, label_file_paths = self.get_image_and_label_paths(images_folder,
                                                                                labels_folder,
                                                                                subset=subset)
            #rename and copy label files
            self.rename_copy_label_files(label_file_paths, folder, keys)

            #copy_image_files
            self.copy_image_paths(image_file_paths, folder)

    def copy_image_paths(self, image_file_paths, current_folder):
      print(f"Copying {len(image_file_paths)} {current_folder} image files to {self.image_out_folder}...\n#####")

      for img_path in image_file_paths:
        dest = os.path.join(self.image_out_folder, os.path.basename(img_path))
        shutil.copy(img_path, dest)

    def get_image_and_label_paths(self, images_folder, labels_folder, subset=None):

      label_file_paths = [os.path.join(labels_folder, f)
        for f in os.listdir(labels_folder) if f.endswith(".txt")]

      image_file_paths = [os.path.join(images_folder, f)
        for f in os.listdir(images_folder) if f.endswith(IMAGE_EXTS)]

      if subset:
        image_file_paths, label_file_paths  = self.get_random_pairs(image_file_paths, labels_folder, subset)

      return image_file_paths, label_file_paths

    def rename_copy_label_files(self, label_file_paths, current_folder, keys):
      #copy files
      if len(keys) > 1:
          label_key = self.remove_numbers(current_folder)
      else:
          label_key = keys[0]

      print(f'#####\nFound {len(label_file_paths)} {current_folder} files'
            f'\nRenaming class id to {self.label_id_map[label_key]}\n'
            f'copying to {self.ann_out_folder}')

      for label_path in label_file_paths:
          outpath = os.path.join(self.ann_out_folder, os.path.basename(label_path))
          self.rename_first_element(label_path, self.label_id_map[label_key], outpath)

    def build_label_id_map(self):
        """
        Builds a mapping between labels and their IDs using the train folders dictionary.

        Returns:
        - label_id_map: Dictionary containing the label-to-ID mapping.
        """
        label_id_map = {}
        for index, folder_label in enumerate(self.label_path_map):
            if self.single_class:
                label_id_map[self.single_class] = 0
            else:
                # Remove numbers from the label
                label = self.remove_numbers(folder_label)
                label_id_map[label] = index

        # If numbers are found, ensure values increment by one
        for index, key in enumerate(label_id_map.keys()):
            label_id_map[key] = index

        return label_id_map

    def split(self, split_folder=None, train_ratio=.7, val_ratio=.2, test_ratio=.1):
        if not split_folder:
            split_folder=self.split_folder
        assert os.path.exists(split_folder), 'Invalid split folder passed'

        return split_folder_into_train_val_test(image_folder=self.image_out_folder,
                                                ann_folder=self.ann_out_folder,
                                                output_folder=split_folder,
                                                train_ratio=train_ratio,
                                                val_ratio=val_ratio,
                                                test_ratio=test_ratio)

    def write_yaml(self, outdir, split_folder=None):
        """
        returns the path to yaml
        :param outdir: save dir
        :param split_folder: where our train/val/test default is None
        :return:
        """
        return write_data_yaml_file(self.class_labels, outdir, dataset_folder=split_folder)

    @staticmethod
    def rename_first_element(txt_file, class_id, output_path):
        with open(txt_file, 'r') as file:
            lines = file.readlines()

        renamed_lines = []
        for line in lines:
            elements = line.strip().split()
            if elements:
                elements[0] = str(class_id)
                renamed_lines.append(' '.join(elements))

        with open(output_path, 'w') as file:
            file.write('\n'.join(renamed_lines))

    @staticmethod
    def get_label_path_map(train_folders):
      train_folders_dict = {}
      for folder in train_folders:
        if folder != '.ipynb_checkpoints':
          label = os.path.basename(folder)
          train_folders_dict[label] = folder

      return train_folders_dict

    @staticmethod
    def remove_numbers(string):
        result = re.sub(r'\d+', '', string)
        return result


    #get a random image file, then check to see if its in the label folder
    @staticmethod
    def get_random_pairs(image_files, label_folder, subset):

        # if not image_files or not ann_files:
        #     print("One or both folders do not contain any files of the required type.")
        #     return []

        valid_img_files=[]
        valid_ann_files=[]
        attempts = 0

        while len(valid_img_files) < subset and attempts < 100:  # Limit the number of attempts to avoid infinite loops
            img_file = random.choice(image_files)
            #remove ext
            filename = os.path.splitext(os.path.basename(img_file))[0]
            label_file_path = os.path.join(label_folder, filename + '.txt')
            if os.path.exists(img_file) and os.path.exists(label_file_path):
              if img_file not in valid_img_files:
                valid_img_files.append(img_file)
                valid_ann_files.append(label_file_path)

            attempts += 1

        return valid_img_files, valid_ann_files

