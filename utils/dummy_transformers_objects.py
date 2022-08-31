# This file is autogenerated by the command `make fix-copies`, do not edit.
# flake8: noqa
from ..utils import DummyObject, requires_backends


class LDMTextToImagePipeline(metaclass=DummyObject):
    _backends = ["transformers"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["transformers"])


class StableDiffusionImg2ImgPipeline(metaclass=DummyObject):
    _backends = ["transformers"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["transformers"])


class StableDiffusionInpaintPipeline(metaclass=DummyObject):
    _backends = ["transformers"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["transformers"])


class StableDiffusionPipeline(metaclass=DummyObject):
    _backends = ["transformers"]

    def __init__(self, *args, **kwargs):
        requires_backends(self, ["transformers"])
