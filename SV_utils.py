#viewing predictions on test set
import supervision as sv

#vis util
def annotate_frame(box_annotator, dataset, key, labels=None):
  """
  returns annotated frame with bbox annotations
  """
  return box_annotator.annotate(
        scene=dataset.images[key].copy(),
        detections=dataset.annotations[key],
        labels=labels)


def get_predictions_from_dataset(dataset,  model, mode=None, conf=0.5,iou=.2, image_folder=None):
  """
  make predictions on a data set with a model trained with the supergradients lib
  or the ultralytics lib. the format of the results differ slightly so we need
  two seperate methods.

  dataset: class from supervision where we can easily load our data in
  model: our working model trained with NAS or ultralytics
  mode: nas or ultra. set to the model lib
  conf: confidence threshold
  iou: iou thresh
  image_folder:
  """
  modes=['nas', 'ultra']
  assert mode in modes, 'Must pass nas or ultra in mode arg'

  if mode=='nas':
    predictions = get_predictions_from_nas(dataset=dataset,
                                           model=model,
                                           conf=conf,
                                           iou=iou)
    return predictions

  if mode=='ultra':
    #assert image_folder, 'Must pass image folder when using mode ULTRA'
    predictions = get_predictions_from_ultra(dataset=dataset,
                                             model=model,
                                             conf=conf,
                                             iou=iou,
                                             image_folder=image_folder)
    return predictions

  return 'no predictions found'


def get_predictions_from_nas(dataset, model, conf, iou):
  predictions = {}

  for image_name, image in dataset.images.items():
    result = list(model.predict(image, conf=conf, iou=iou))[0]
    detections = sv.Detections(
        xyxy=result.prediction.bboxes_xyxy,
        confidence=result.prediction.confidence,
        class_id=result.prediction.labels.astype(int)
    )
    predictions[image_name] = detections
  return predictions


def get_predictions_from_ultra(dataset, model, conf, iou, image_folder):
    predictions = {}

    for image_name, image in dataset.images.items():
      #image_path = os.path.join(image_folder, image_name)
      result = list(model.predict(source=image, conf=conf, iou=iou))[0]
      detections = sv.Detections(
          xyxy=result.boxes.xyxy.cpu().numpy(),
          confidence=result.boxes.conf.cpu().numpy(),
          class_id=result.boxes.cls.cpu().numpy().astype(int)
      )
      predictions[image_name] = detections
    return predictions