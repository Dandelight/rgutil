import torch
from torch import Tensor
from torch import nn
from torch.nn.functional import normalize


class CentroidClassifier(nn.Module):
    """Just forward it, without softmax or cross entropy loss."""
    def __init__(self) -> None:
        super().__init__()

    def set_centroid_by_features_and_targets(self, features, targets):
        """
        Args:
            features: (N, C)
            targets: (N)
        """
        centroids = torch.zeros((targets.max() + 1, features.size(1)), device=features.device)
        for i in range(targets.max() + 1):
            centroids[i] = features[targets == i].mean(dim=0)
        self.set_centroid(centroids)

    def set_centroid(self, centroid):
        self.centroids = normalize(centroid)

    def forward(self, inputs: Tensor):
        outputs = inputs.mm(self.centroids.t())
        return outputs
