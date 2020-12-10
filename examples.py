"""
Module use examples

Requires:
    opencv-python, numpy
"""
import cv2
import numpy as np

from lapixdl.evaluation.evaluate import evaluate_segmentation, evaluate_classification, evaluate_detection
from lapixdl.evaluation.visualize import show_segmentation, show_classifications, show_detections
from lapixdl.evaluation.model import BBox, Classification, Result


def main():
    # Model evaluation examples
    evaluate_segmentation_example()
    evaluate_detection_example()
    evaluate_classification_example()

    show_classification_example()


def evaluate_segmentation_example():
    # Class names - Background must be at 0 index
    classes = ['bkg', 'kite', 'person']

    # Image shape
    mask_shape = (480, 640)

    # Creating fake data
    # Creates a rectangle of 1s in a 0s array
    gt_bbox_1 = BBox(10, 10, 10, 10, 1)
    mask_bin_GT_1 = cv2.rectangle(np.zeros(mask_shape, np.int),
                                  gt_bbox_1.upper_left_point,
                                  gt_bbox_1.bottom_right_point,
                                  1, -1)

    pred_bbox_1 = BBox(10, 10, 10, 10, 1)
    mask_bin_pred_1 = cv2.rectangle(np.zeros(mask_shape, np.int),
                                    pred_bbox_1.upper_left_point,
                                    pred_bbox_1.bottom_right_point,
                                    1, -1)

    # Creates a rectangle of 2s in a 0s array
    gt_bbox_2 = BBox(110, 110, 320, 280, 2)
    mask_bin_GT_2 = cv2.rectangle(np.zeros(mask_shape, np.int),
                                  gt_bbox_2.upper_left_point,
                                  gt_bbox_2.bottom_right_point,
                                  2, -1)

    pred_bbox_2 = BBox(70, 50, 240, 220, 2)
    mask_bin_pred_2 = cv2.rectangle(np.zeros(mask_shape, np.int),
                                    pred_bbox_2.upper_left_point,
                                    pred_bbox_2.bottom_right_point,
                                    2, -1)

    # Merging masks
    mask_GT = np.maximum(mask_bin_GT_1, mask_bin_GT_2)
    mask_pred = np.maximum(mask_bin_pred_1, mask_bin_pred_2)

    # Creating data suplier iterator
    # It is not necessary here, but it's useful if you want to yield data
    # from the disk i.e. from a Pytorch DataLoader
    it_gt_masks = identity_iterator(mask_GT)
    it_pred_masks = identity_iterator(mask_pred)

    # Calculates and shows metrics
    metrics = evaluate_segmentation(it_gt_masks, it_pred_masks, classes)

    # Shows confusion matrix and returns its Figure and Axes
    fig, axes = metrics.show_confusion_matrix()

    # Shows confusion matrix for class `a`
    metrics.by_class[0].show_confusion_matrix()


def evaluate_detection_example():
    # Class names
    classes = ['kite', 'person']

    # Image shape
    mask_shape = (480, 640)

    # Creating fake data
    gt_bbox_1 = BBox(10, 10, 10, 10, 0)
    pred_bbox_1 = BBox(10, 10, 10, 10, 0)

    gt_bbox_2 = BBox(110, 110, 320, 280, 1)
    pred_bbox_2 = BBox(70, 50, 240, 220, 1)

    # Creating data suplier iterator
    # It is not necessary here, but it's useful if you want to yield data
    # from the disk i.e. from a Pytorch DataLoader
    it_gt_masks = identity_iterator([gt_bbox_1, gt_bbox_2])
    it_pred_masks = identity_iterator([pred_bbox_1, pred_bbox_2])

    # Calculates and shows metrics
    metrics = evaluate_detection(it_gt_masks, it_pred_masks, classes)

    # Shows confusion matrix and returns its Figure and Axes
    fig, axes = metrics.show_confusion_matrix()

    # Shows confusion matrix for class `a`
    metrics.by_class[0].show_confusion_matrix()


def evaluate_classification_example():
    # Class names
    classes = ['a', 'b', 'c']

    # Classifications based in array
    gt_class = [Classification(x) for x in [
        0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
    # All predictions with .8 score
    pred_class = [Classification(x, .8) for x in [
        0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 2]]

    # Calculates and shows metrics
    metrics = evaluate_classification(gt_class, pred_class, classes)

    # Shows confusion matrix and returns its Figure and Axes
    fig, axes = metrics.show_confusion_matrix()

    # Shows confusion matrix for class `a`
    metrics.by_class[0].show_confusion_matrix()


def show_classification_example():
    # Class names
    classes = ['a', 'b', 'c']

    # Classifications based in array
    gt_class = [Classification(x) for x in [
        0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
    # All predictions with .8 score
    pred_class = [Classification(x, .8) for x in [
        0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 2]]

    # Calculates and shows metrics
    results = [Result((np.random.rand(200, 400, 3) * 125).astype(np.int8), gt, pred)
               for gt, pred in zip(gt_class, pred_class)]

    # Shows confusion matrix and returns its Figure and Axes
    fig, axes = show_classifications(results, classes, 5)


def identity_iterator(value):
    yield value


main()
