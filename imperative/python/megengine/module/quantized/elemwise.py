# MegEngine is Licensed under the Apache License, Version 2.0 (the "License")
#
# Copyright (c) 2014-2020 Megvii Inc. All rights reserved.
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT ARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from ...core.ops._internal import param_defs as P
from ...functional.elemwise import _elemwise_multi_type
from ...tensor import Tensor
from ..qat import elemwise as QAT
from .module import QuantizedModule


class Elemwise(QuantizedModule):
    r"""Quantized version of :class:`~.qat.elemwise.Elemwise`."""

    _elemwise_multi_type_mode = P.ElemwiseMultiType.Mode

    def __init__(self, method, dtype=None):
        super().__init__()
        self.method = self._elemwise_multi_type_mode.convert("Q" + method)
        self.output_dtype = dtype

    def forward(self, *inps):
        if self.training:
            raise ValueError("quantized module only support inference.")
        return _elemwise_multi_type(*inps, mode=self.method, dtype=self.output_dtype)

    @classmethod
    def from_qat_module(cls, qat_module: QAT.Elemwise):
        r"""
        Return a :class:`~.QuantizedModule` instance converted from a
        :class:`~.QATModule` instance.
        """
        return cls(qat_module.method.name, qat_module.get_activation_dtype())
