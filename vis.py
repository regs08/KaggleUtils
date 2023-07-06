#vis utils. preparing the frame for a grid comparison

import random
import supervision as sv
import cv2
from matplotlib import pyplot as plt


def prepare_images_pred_frames(keys, dataset, predictions, id_to_label, box_annotator, apply_mask=False):
  """
  getting our image and prediction frames to use in plot images grid
  """
  images = []
  titles = []
  for key in keys:
      current_ann=dataset.annotations[key]
      gt_labels = [id_to_label[id] for id in current_ann.class_id]

      frame_with_annotations = box_annotator.annotate(
          scene=dataset.images[key].copy(),
          detections=current_ann,
          labels=gt_labels
      )

      if apply_mask:
          mask_annotator = sv.MaskAnnotator()
          frame_with_annotations = mask_annotator.annotate(
              scene=frame_with_annotations,
              detections=current_ann
          )
      images.append(frame_with_annotations)
      titles.append('annotations')
      current_pred = predictions[key]
      pred_labels=[id_to_label[id] for id in current_pred.class_id]


      frame_with_predictions = box_annotator.annotate(
          scene=dataset.images[key].copy(),
          detections= current_pred,
          labels=pred_labels
      )
      if apply_mask:
          mask_annotator = sv.MaskAnnotator()
          frame_with_predictions = mask_annotator.annotate(
              scene=frame_with_predictions,
              detections=current_pred
          )
      images.append(frame_with_predictions)
      titles.append('predictions')
  return images, titles


def plot_rand_img_from_dataset_with_sv(ds, id_label_map, box_annotator=False, seed=None, size=(10, 10)):
    # getting a random key
    if seed:
        random.seed(seed)
    RAND_IMG = random.sample(list(ds.images.keys()), 1)[0]
    print(f'Random image filename: {RAND_IMG}')

    # default box_annotator
    if not box_annotator:
        box_annotator = sv.BoxAnnotator(thickness=5,
                                        color=sv.Color(255, 0, 0),
                                        text_scale=1.0,
                                        text_thickness=2)
    # labels of the image
    labels = [id_label_map[id] for id in ds.annotations[RAND_IMG].class_id]

    frame = box_annotator.annotate(
        scene=ds.images[RAND_IMG].copy(),
        detections=ds.annotations[RAND_IMG],
        labels=labels)

    plt.figure(figsize=size)
    plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


def annotate_mask(ds, img_name, id_label_map, mask_annotator=None, box_annotator=None):
    """

    :param img_name: basename of the iamge file
    :param mask_annotator: annotator helper from supervision. default values are provided
    :param box_annotator: annotator helper from supervision. default values are provided
    :return: np array with our mask/box annotations
    """
    if not mask_annotator:
        mask_annotator = sv.MaskAnnotator()
    if not box_annotator:
        box_annotator = sv.BoxAnnotator(thickness=5, text_scale=1.0, text_thickness=2)

    frame_with_boxes = box_annotator.annotate(
        scene=ds.images[img_name].copy(),
        detections=ds.annotations[img_name],
        labels=[id_label_map[id] for id in ds.annotations[img_name].class_id]
    )

    frame = mask_annotator.annotate(
        scene=frame_with_boxes,
        detections=ds.annotations[img_name]
    )
    return frame