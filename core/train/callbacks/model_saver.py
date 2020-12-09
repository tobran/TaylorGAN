import os
from typing import Dict

import tensorflow as tf
from serving_utils import Saver

from library.utils import format_path

from .base import Callback


class ModelSaver(Callback):

    def __init__(self, signature, directory: str, period: int):
        self.signature = signature
        self.directory = directory
        if period <= 0:
            raise ValueError("'saving_period' should be positive!")
        self.period = period

    def on_train_begin(self, logs: Dict = None):
        os.makedirs(self.directory, exist_ok=True)

    def on_epoch_end(self, epoch):
        if epoch % self.period == 0:
            path = os.path.join(self.directory, f"tf_model_epo{epoch}")
            print(f"{epoch} epochs done. Save model to {path}.")
            os.makedirs(path, exist_ok=True)
            Saver(
                session=tf.get_default_session(),
                output_dir=path,
                signature_def_map=self.signature,
            ).save()

    def __str__(self):
        return f"{self.__class__.__name__}(dir={format_path(self.directory)}, period={self.period})"
