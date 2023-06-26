#util functions
import os
import yaml


def write_data_yaml_file(class_labels, outdir, dataset_folder=None):
    """
    writes a yaml file with or without the train/val/test paths via dataset_folder arg
    :param DIRS: dict containing our  train, val, test, paths
    :param class_labels: class labels used for training
    :param outdir: save dir for the yaml file
    :return: yaml path
    """
    if dataset_folder:
      train_dir = os.path.join(dataset_folder, 'train')
      val_dir = os.path.join(dataset_folder,  'val')
      test_dir = os.path.join(dataset_folder, 'test')
      yaml_dict = {'train': train_dir,
                  'val': val_dir,
                  'test': test_dir,
                  'nc': len(class_labels),
                  'names': class_labels}
    else:
      yaml_dict = {'nc': len(class_labels),
                 'names': class_labels}

    yaml_path = os.path.join(outdir, 'data.yaml')
    with open(yaml_path, 'w') as file:
        documents = yaml.dump(yaml_dict, file)
    return yaml_path
