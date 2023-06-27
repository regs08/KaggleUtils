import os
import shutil
import re
from KaggleUtils.ManagingFiles.split_folder import split_folder_into_train_val_test
"""
  here we build our trainset. we iterate through the list of train folders -label
  name with two sub folders, images and labels- to move the files to a folder
  then they will be split into train val and test sets. images and anns will be 
  copied to the out folders provided in the constructor
"""


class TrainSetBuilder:
    def __init__(self, train_folders, image_folder, ann_folder, single_class=None):

        self.train_folders_dict = self.get_train_folders_as_dict(train_folders)
        self.image_folder = image_folder
        self.ann_folder = ann_folder
        self.single_class = single_class
        self.label_to_id_map = self.build_label_id_map()

    def build_train_set(self):
        keys = list(self.label_to_id_map.keys())
        for folder in self.train_folders_dict:
            print(f"Copying {folder} ann files to {self.ann_folder}...")
            labels_folder = os.path.join(self.train_folders_dict[folder], "labels")
            assert os.path.isdir(labels_folder), f'Invalid folder \n {labels_folder}'

            if len(keys) > 1:
                label_key = self.remove_numbers(folder)
            else:
                label_key = keys[0]

            ann_files = [os.path.join(labels_folder, f) for f in os.listdir(labels_folder) if f.endswith(".txt")]
            print(f'Found {len(ann_files)} {folder} files\nRenaming class id to {self.label_to_id_map[label_key]}')
            for ann_path in ann_files:
                outpath = os.path.join(self.ann_folder, os.path.basename(ann_path))
                self.rename_first_element(ann_path, self.label_to_id_map[label_key], outpath)

            print(f"Copying {folder} image files to {self.image_folder}...\n")
            images_folder = os.path.join(self.train_folders_dict[folder], "images")
            assert os.path.isdir(images_folder), f'Invalid folder \n {images_folder}'

            for f in os.listdir(images_folder):
                if f.endswith((".jpg", ".jpeg", ".png", ".gif")):
                    img_file = os.path.join(images_folder, f)
                    dest = os.path.join(self.image_folder, f)
                    shutil.copy(img_file, dest)

    def rename_first_element(self, txt_file, class_id, output_path):
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

    def build_label_id_map(self):
        """
        Builds a mapping between labels and their IDs using the train folders dictionary.

        Returns:
        - label_id_map: Dictionary containing the label-to-ID mapping.
        """
        label_id_map = {}
        for index, folder_label in enumerate(self.train_folders_dict):
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

    def split(self, outfolder):
        return split_folder_into_train_val_test(image_folder=self.image_folder,
                                         ann_folder=self.ann_folder,
                                         output_folder=outfolder)

    @staticmethod
    def get_train_folders_as_dict(train_folders):
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

