import torch
import torch.nn as nn
import torch.nn.functional as F


__all__ = []


def log_with_zeros(x):
    """
    Log with zeros in x.
    """
    x = torch.max(x, torch.tensor(1e-10))
    return torch.log(x)
