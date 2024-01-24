# Utilities from Raymond Guo

This repository contains a set of Python utilities, written or collected, widely used and (hopefully) thoroughly tested, for the faster development of new [`torch`](https://pytorch.org/)-based projects.

The repository contains:

* ~~`cvtv` package for `OpenCV`-based `torchvision` transformations, forked from <https://github.com/hityzy1122/opencv_transforms_torchvision/>.~~ Deprecated in favor of [Albumentations](https://albumentations.ai/)
* `log` package for `get_logger`.
* `loss.robust` from <https://github.com/HanxunH/Active-Passive-Losses/>.
* `model.centroid` for `CentroidClassifier`.
* `torchsnooper` to print the shapes of `torch.Tensor`s without entering debug mode.
* `cluster_accuracy` for an accuracy score with Hungarian algorithm.
* `io` for loading or saving models.
* `mail` for mailing utilities.
* `plot` for plottig utilities
* `selfpatch` for generating `Git` patches for the script itself for each run.
