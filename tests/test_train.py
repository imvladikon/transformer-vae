import logging
import sys
from unittest.mock import patch
import torch
from transformers.testing_utils import TestCasePlus, torch_device

from t5_vae.train import main


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()


class TrainTests(TestCasePlus):
    def test_train_txt(self):
        """
        Does a test training run and checks it works.
        """
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --do_eval
            --per_device_train_batch_size 4
            --per_device_eval_batch_size 4
            --num_train_epochs 2
            --set_seq_size 4
            --latent_size 2
            --t5_model_name t5-small
            --output_dir {tmp_dir}
            --overwrite_output_dir
            """.split()

        if torch.cuda.device_count() > 1:
            # Skipping because there are not enough batches to train the model + would need a drop_last to work.
            return

        if torch_device != "cuda":
            testargs.append("--no_cuda")

        with patch.object(sys, "argv", testargs):
            result = main()
            self.assertAlmostEqual(result["epoch"], 2.0)

    def test_train_csv(self):
        """
        Does a test training run and checks it works.
        """
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/multiline_max_len_4.csv
            --validation_file ./tests/fixtures/multiline_max_len_4.csv
            --do_train
            --do_eval
            --per_device_train_batch_size 5
            --per_device_eval_batch_size 5
            --num_train_epochs 2
            --set_seq_size 5
            --output_dir {tmp_dir}
            --overwrite_output_dir
            """.split()

        if torch.cuda.device_count() > 1:
            # Skipping because there are not enough batches to train the model + would need a drop_last to work.
            return

        if torch_device != "cuda":
            testargs.append("--no_cuda")

        with patch.object(sys, "argv", testargs):
            result = main()
            self.assertAlmostEqual(result["epoch"], 2.0)

    def test_train_json(self):
        """
        Does a test training run and checks it works.
        """
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/max_len_3.json
            --validation_file ./tests/fixtures/max_len_3.json
            --do_train
            --do_eval
            --per_device_train_batch_size 5
            --per_device_eval_batch_size 5
            --num_train_epochs 2
            --set_seq_size 4
            --output_dir {tmp_dir}
            --overwrite_output_dir
            """.split()

        if torch.cuda.device_count() > 1:
            # Skipping because there are not enough batches to train the model + would need a drop_last to work.
            return

        if torch_device != "cuda":
            testargs.append("--no_cuda")

        with patch.object(sys, "argv", testargs):
            result = main()
            self.assertAlmostEqual(result["epoch"], 2.0)