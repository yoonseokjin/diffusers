# Copyright 2023 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..utils import _LazyModule, is_flax_available, is_torch_available


_import_structure = {}

if is_torch_available():
    _import_structure["adapter"] = ["MultiAdapter", "T2IAdapter"]
    _import_structure["autoencoder_asym_kl"] = ["AsymmetricAutoencoderKL"]
    _import_structure["autoencoder_kl"] = ["AutoencoderKL"]
    _import_structure["autoencoder_tiny"] = ["AutoencoderTiny"]
    _import_structure["controlnet"] = ["ControlNetModel"]
    _import_structure["dual_transformer_2d"] = ["DualTransformer2DModel"]
    _import_structure["modeling_utils"] = ["ModelMixin"]
    _import_structure["prior_transformer"] = ["PriorTransformer"]
    _import_structure["t5_film_transformer"] = ["T5FilmDecoder"]
    _import_structure["transformer_2d"] = ["Transformer2DModel"]
    _import_structure["transformer_temporal"] = ["TransformerTemporalModel"]
    _import_structure["unet_1d"] = ["UNet1DModel"]
    _import_structure["unet_2d"] = ["UNet2DModel"]
    _import_structure["unet_2d_condition"] = ["UNet2DConditionModel"]
    _import_structure["unet_3d_condition"] = ["UNet3DConditionModel"]
    _import_structure["vq_model"] = ["VQModel"]

if is_flax_available():
    _import_structure["controlnet_flax"] = ["FlaxControlNetModel"]
    _import_structure["unet_2d_condition_flax"] = ["FlaxUNet2DConditionModel"]
    _import_structure["vae_flax"] = ["FlaxAutoencoderKL"]

import sys


sys.modules[__name__] = _LazyModule(__name__, globals()["__file__"], _import_structure, module_spec=__spec__)
