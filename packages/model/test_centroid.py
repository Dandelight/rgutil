from centroid import CentroidClassifier

import torch


def test_centroid_classifier():
    """Pytest function for testing the :class:`CentroidClassifier`."""

    cls = CentroidClassifier()
    cls.set_centroid(torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32))
    inputs = torch.tensor([[1, 2, 3], [4, 5, 6]], dtype=torch.float32)
    outputs = cls(inputs)
    assert outputs.shape == (2, 2)


def test_set_center():
    """Set centers by classes and features"""
    cls = CentroidClassifier()
    features = torch.tensor([[1, 2, 3], [-4, -5, -6]], dtype=torch.float32)
    features = torch.nn.functional.normalize(features, dim=1)
    labels = torch.tensor([0, 1], dtype=torch.int64)
    cls.set_centroid_by_features_and_targets(
        features,
        labels,
    )

    inputs = torch.tensor([[1, -2, -1], [4, 4, 5]], dtype=torch.float32)
    inputs = torch.nn.functional.normalize(inputs, dim=1)
    outputs = cls(inputs)
    assert torch.allclose(outputs, torch.tensor([[-0.6547,  0.5583], [0.9558, -0.9962]], dtype=torch.float32), atol=1e-3)

    pred = torch.softmax(outputs, dim=1).argmax(dim=1)
    assert torch.all(pred == torch.tensor([1, 0], dtype=torch.int64))
