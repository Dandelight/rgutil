"""
the functions read_json, write_json, save_checkpoint, load_checkpoint, copy_state_dict are provided by https://github.com/alibaba/cluster-contrast-reid under the MIT license.
"""

import json
import os
import os.path as osp
import shutil
import torch


def read_json(fpath):
    with open(fpath, "r") as f:
        obj = json.load(f)
    return obj


def write_json(obj, fpath):
    os.makedirs(osp.dirname(fpath), exist_ok=True)
    with open(fpath, "w") as f:
        json.dump(obj, f, indent=4, separators=(",", ": "), ensure_ascii=False)


def save_checkpoint(state, is_best, fpath="checkpoint.pth.tar"):
    os.makedirs(osp.dirname(fpath), exist_ok=True)
    torch.save(state, fpath)
    if is_best:
        shutil.copy(fpath, osp.join(osp.dirname(fpath), "model_best.pth.tar"))


def load_checkpoint(fpath):
    if osp.isfile(fpath):
        # checkpoint = torch.load(fpath)
        checkpoint = torch.load(fpath, map_location=torch.device("cpu"))
        print("=> Loaded checkpoint '{}'".format(fpath))
        return checkpoint
    else:
        raise ValueError("=> No checkpoint found at '{}'".format(fpath))


def copy_state_dict(state_dict, model, strip_prefix=None):
    tgt_state = model.state_dict()
    copied_names = set()
    unused = set()

    for name, param in state_dict.items():
        if strip_prefix is not None and name.startswith(strip_prefix):
            name = name[len(strip_prefix) :]
        if name not in tgt_state:
            unused.add(name)
            continue
        if isinstance(param, torch.nn.Parameter):
            param = param.data
        if param.size() != tgt_state[name].size():
            print("mismatch:", name, param.size(), tgt_state[name].size())
            continue
        tgt_state[name].copy_(param)
        copied_names.add(name)

    missing = set(tgt_state.keys()) - copied_names

    if len(unused) > 0:
        print("unused checkpoint keys:", unused)
    if len(missing) > 0:
        print("missing keys in source state_dict:", missing)

    return model
