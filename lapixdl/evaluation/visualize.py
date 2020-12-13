from typing import Optional, Union, List, Tuple, TypeVar, Generic
import math

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import seaborn as sn

from .model import BBox, Mask, Classification, Result

correct_color = sn.color_palette("Paired")[3]
incorrect_color = sn.color_palette("Paired")[5]


def show_classifications(
        results: List[Result[Classification]],
        class_names: List[str],
        cols: int = 3,
        diff_correct_incorect: bool = True) -> Tuple[Figure, Axes]:
    """Shows multiple classification results.

    Args:
        results (List[Result[Classification]]): List of classification results.
        class_names (List[str]): Class names.
        cols (int, optional): Number of colunms to show. Defaults to 3.
        diff_correct_incorect (bool, optional): Indicates if correct and incorrect 
        results should be differentiated by color. Defaults to True.

    Returns:
        Tuple[Figure, Axes]: Figure and Axes of the ploted results.
    """

    rows = math.ceil(len(results) / cols)
    fig, axes = plt.subplots(rows, cols)
    fig.suptitle('Classifications')

    for i, result in enumerate(results):
        axis = axes[i // cols][i % cols]
        axis.set_title(
            f'GT: {class_names[result.gt.cls]}' +
            (f'\nPred: {class_names[result.prediction.cls]} ({result.prediction.score})' if not result.prediction is None else ''),
            fontsize='small',
            color='#333' if result.prediction is None or not diff_correct_incorect
            else (correct_color if result.prediction.cls ==
                  result.gt.cls else incorrect_color)
        )
        axis.axis('off')
        axis.imshow(result.image)

    for i in range(len(results), (cols * rows)):
        axis = axes[i // cols][i % cols]
        axis.axis('off')

    plt.tight_layout(w_pad=.2, h_pad=1.5)
    plt.show()
    return fig, axes


def show_segmentation(
        results: List[Result[Mask]],
        class_names: List[str],
        cols: int = 1,
        palette: Optional[str] = None) -> Tuple[Figure, Axes]:

    rows = math.ceil(len(results) / cols)
    fig, ax = plt.subplots()
    fig.suptitle('Segmentations')

    cmap = sn.color_palette(palette)

    plt.show()
    return fig, ax


def show_detections(results: List[Result[List[BBox]]]) -> Tuple[Figure, Axes]:
    fig, ax = plt.subplots()
    fig.suptitle('Detections')

    plt.show()
    return fig, ax
