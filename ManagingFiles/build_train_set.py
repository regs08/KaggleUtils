import os
import shutil


def build_train_set(train_folders_dict, image_folder, ann_folder, label_to_id_map):
  """
  here we build our trainset. we iterate through the train folders dict to obtain
  the label(key) and the path(value) we then rename all of the annotations to either
  0 (grape detection) or a unique class id per label (detection and classification)
  """
  image_paths = []

  for label in train_folders_dict:
      print(f"Moving {label} ann files to {ann_folder}...")
      labels_folder = os.path.join(train_folders_dict[label], "labels")
      assert os.path.isdir(labels_folder), f'Invalid folder \n {labels_folder}'

      #get ann files from folder
      ann_files = [os.path.join(labels_folder, f) for f in os.listdir(labels_folder) if f.endswith(".txt")]
      #change the class id for the files.by default they are all 0
      print(f'Found {len(ann_files)} {label} files\nRenaming class id to {label_to_id_map[label]}')
      for ann_path in ann_files:
        outpath=os.path.join(ann_folder, os.path.basename(ann_path))
        rename_first_element(ann_path, label_to_id_map[label], outpath)

      print(f"Copying {label} image files to {image_folder}...")
      images_folder = os.path.join(train_folders_dict[label], "images")
      assert os.path.isdir(images_folder), f'Invalid folder \n {images_folder}'

      for f in os.listdir(images_folder):
        if f.endswith((".jpg", ".jpeg", ".png", ".gif")):
          img_file = os.path.join(images_folder, f)
          dest=os.path.join(image_folder, f)
          shutil.copy(img_file, dest)


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


def get_train_folders_as_dict(train_folders):

  #expected layout is the folder will be named as the class label with two subfolders
  #images and labels, where folder name. is the same as the class
  folders = []
  for dir in train_folders:
    #getting all the folders
    folders.extend([os.path.join(dir, folder) for folder in os.listdir(dir)])

  train_folders = {}
  for f in folders:
    label=os.path.basename(f)
    if label != '.ipynb_checkpoints':
      train_folders[label] = f

  return train_folders