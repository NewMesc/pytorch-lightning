import inspect

from pytorch_lightning import Callback
from pytorch_lightning import Trainer, LightningModule
from tests.base import EvalModelTemplate


def test_trainer_callback_system(tmpdir):
    """Test the callback system."""

    hparams = EvalModelTemplate.get_default_hparams()
    model = EvalModelTemplate(**hparams)

    def _check_args(trainer, pl_module):
        assert isinstance(trainer, Trainer)
        assert isinstance(pl_module, LightningModule)

    class TestCallback(Callback):
        def __init__(self):
            super().__init__()
            self.called = []

        def setup(self, trainer, pl_module, stage: str):
            self.called.append(inspect.currentframe().f_code.co_name)
            assert isinstance(trainer, Trainer)

        def teardown(self, trainer, pl_module, step: str):
            self.called.append(inspect.currentframe().f_code.co_name)
            assert isinstance(trainer, Trainer)

        def on_init_start(self, trainer):
            self.called.append(inspect.currentframe().f_code.co_name)
            assert isinstance(trainer, Trainer)

        def on_init_end(self, trainer):
            self.called.append(inspect.currentframe().f_code.co_name)
            assert isinstance(trainer, Trainer)

        def on_fit_start(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            assert isinstance(trainer, Trainer)

        def on_fit_end(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            assert isinstance(trainer, Trainer)

        def on_sanity_check_start(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_sanity_check_end(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_epoch_start(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_epoch_end(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_batch_start(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_batch_end(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_train_batch_start(self, trainer, pl_module, batch, batch_idx, dataloader_idx):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_train_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_validation_batch_start(self, trainer, pl_module, batch, batch_idx, dataloader_idx):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_validation_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_test_batch_start(self, trainer, pl_module, batch, batch_idx, dataloader_idx):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_test_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_train_start(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_train_end(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_pretrain_routine_start(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_pretrain_routine_end(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_validation_start(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_validation_end(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_test_start(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

        def on_test_end(self, trainer, pl_module):
            self.called.append(inspect.currentframe().f_code.co_name)
            _check_args(trainer, pl_module)

    test_callback = TestCallback()

    trainer_options = dict(
        default_root_dir=tmpdir,
        callbacks=[test_callback],
        max_epochs=1,
        limit_val_batches=1,
        limit_train_batches=3,
        limit_test_batches=2,
        progress_bar_refresh_rate=0,
    )

    # no call yet
    assert len(test_callback.called) == 0

    # fit model
    trainer = Trainer(**trainer_options)

    # check that only the to calls exists
    assert trainer.callbacks[0] == test_callback
    assert test_callback.called == [
        'on_init_start',
        'on_init_end',
    ]

    trainer.fit(model)

    assert test_callback.called[2:] == [
        'setup',
        'on_fit_start',
        'on_pretrain_routine_start',
        'on_pretrain_routine_end',
        'on_sanity_check_start',
        'on_validation_start',
        'on_validation_batch_start',
        'on_validation_batch_end',
        'on_validation_end',
        'on_sanity_check_end',
        'on_train_start',
        'on_epoch_start',
        'on_batch_start',
        'on_train_batch_start',
        'on_batch_end',
        'on_train_batch_end',
        'on_batch_start',
        'on_train_batch_start',
        'on_batch_end',
        'on_train_batch_end',
        'on_batch_start',
        'on_train_batch_start',
        'on_batch_end',
        'on_train_batch_end',
        'on_validation_start',
        'on_validation_batch_start',
        'on_validation_batch_end',
        'on_validation_end',
        'on_epoch_end',
        'on_train_end',
        'on_fit_end',
        'teardown'
    ]

    test_callback = TestCallback()
    trainer_options.update(callbacks=[test_callback])
    trainer = Trainer(**trainer_options)
    trainer.test(model)

    assert test_callback.called == [
        'on_init_start',
        'on_init_end',
        'setup',
        'on_fit_start',
        'on_pretrain_routine_start',
        'on_pretrain_routine_end',
        'on_test_start',
        'on_test_batch_start',
        'on_test_batch_end',
        'on_test_batch_start',
        'on_test_batch_end',
        'on_test_end',
        'on_fit_end',
        'teardown',
        'teardown',
    ]
