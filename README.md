# Utilities from Raymond Guo

```plaintext
       ____                                        __   ______
      / __ \____ ___  ______ ___  ____  ____  ____/ /  / ____/_______  ___  ____
     / /_/ / __ `/ / / / __ `__ \/ __ \/ __ \/ __  /  / / __/ ___/ _ \/ _ \/ __ \
    / _, _/ /_/ / /_/ / / / / / / /_/ / / / / /_/ /  / /_/ / /  /  __/  __/ / / /
   /_/ |_|\__,_/\__, /_/ /_/ /_/\____/_/ /_/\__,_/   \____/_/   \___/\___/_/ /_/
               /____/
```

ASCII Art generated by <https://patorjk.com/software/taag/#p=display&f=Slant&t=%20Raymond%20Green>.

This repository contains a set of utilities, written or collected, widely used and (hopefully) thoroughly tested, for the faster development of new projects.

The repository contains:

## Python

* `log` package for `get_logger`.
* `loss.robust` from <https://github.com/HanxunH/Active-Passive-Losses/>.
* `model.centroid` for `CentroidClassifier`.
* `torchsnooper` to print the shapes of `torch.Tensor`s without entering debug mode.
* `cluster_accuracy` for an accuracy score with Hungarian algorithm.
* `io` for loading or saving models.
* `mail` for mailing utilities.
* `plot` for plottig utilities
* `selfpatch` for generating `Git` patches for the script itself for each run.
* ~~`cvtv` package for `OpenCV`-based `torchvision` transformations, forked from <https://github.com/hityzy1122/opencv_transforms_torchvision/>.~~ Deprecated in favor of [Albumentations](https://albumentations.ai/)

## JavaScript

* A crawler

## Shell

* `tmux` background utility.
