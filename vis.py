#vis utils. preparing the frame for a grid comparison


def prepare_images_pred_frames(keys, dataset, predictions, id_to_label, box_annotator):
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
      images.append(frame_with_annotations)
      titles.append('annotations')
      current_pred = predictions[key]
      pred_labels=[id_to_label[id] for id in current_pred.class_id]
      frame_with_predictions = box_annotator.annotate(
          scene=dataset.images[key].copy(),
          detections= current_pred,
          labels=pred_labels
      )
      images.append(frame_with_predictions)
      titles.append('predictions')
  return images, titles
