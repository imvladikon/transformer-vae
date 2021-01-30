import logging
import sys
from unittest.mock import patch
import torch
from transformers.testing_utils import TestCasePlus, torch_device

from transformer_vae.train import main


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()


class TrainTests(TestCasePlus):
    def test_train_txt(self):
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
            --set_seq_size 5
            --latent_size 2
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
            --latent_size 2
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
            --latent_size 2
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

    def test_train_python_syntax_seq_check(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --do_eval
            --sample_from_latent
            --per_device_train_batch_size 4
            --per_device_eval_batch_size 4
            --num_train_epochs 1
            --set_seq_size 8
            --n_latent_tokens 1
            --latent_size 2
            --output_dir {tmp_dir}
            --overwrite_output_dir
            --seq_check python
            """.split()

        if torch.cuda.device_count() > 1:
            # Skipping because there are not enough batches to train the model + would need a drop_last to work.
            return

        if torch_device != "cuda":
            testargs.append("--no_cuda")

        with patch.object(sys, "argv", testargs):
            result = main()
            self.assertAlmostEqual(result["epoch"], 1.0)

    def test_train_non_vae(self):
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
            --dont_use_reg_loss
            --encoder_model full-1st-token
            --decoder_model n-tokens
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

    def test_train_unsupervised_classification(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --dataset_name=Fraser/news-category-dataset
            --text_column=headline
            --classification_column=category_num
            --do_eval
            --per_device_train_batch_size 2
            --per_device_eval_batch_size 2
            --max_validation_size 100
            --eval_steps 4
            --encoder_model full-1st-token
            --decoder_model n-tokens
            --latent_size 2
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
            self.assertGreater(result["eval_loss"], 0.0)
            self.assertNotIn("epoch", result)

    def test_train_n_tokens_model(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --per_device_train_batch_size 2
            --num_train_epochs 1
            --set_seq_size 4
            --encoder_model n-tokens
            --n_latent_tokens 2
            --decoder_model n-tokens
            --latent_size 2
            --output_dir {tmp_dir}
            --overwrite_output_dir
            """.split()

        if torch.cuda.device_count() > 1:
            # Skipping because there are not enough batches to train the model + would need a drop_last to work.
            return

        if torch_device != "cuda":
            testargs.append("--no_cuda")

        with patch.object(sys, "argv", testargs):
            main()

    def test_train_unsupervised_classification_agnews(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --dataset_name=ag_news
            --classification_column=label
            --do_train
            --max_steps=10
            --validation_name=test
            --test_classification
            --per_device_train_batch_size 2
            --per_device_eval_batch_size 2
            --max_validation_size 100
            --encoder_model full-1st-token
            --decoder_model n-tokens
            --latent_size 2
            --output_dir {tmp_dir}
            --overwrite_output_dir
            """.split()

        if torch.cuda.device_count() > 1:
            # Skipping because there are not enough batches to train the model + would need a drop_last to work.
            return

        if torch_device != "cuda":
            testargs.append("--no_cuda")

        with patch.object(sys, "argv", testargs):
            main()

    def test_train(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --do_eval
            --eval_steps 3
            --evaluation_strategy steps
            --sample_from_latent
            --per_device_train_batch_size 2
            --per_device_eval_batch_size 2
            --num_train_epochs 1
            --set_seq_size 8
            --encoder_model n-tokens
            --decoder_model n-tokens
            --n_latent_tokens 1
            --latent_size 2
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
            self.assertAlmostEqual(result["epoch"], 1.0)

    def test_train_critic(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --do_eval
            --eval_steps 3
            --evaluation_strategy steps
            --sample_from_latent
            --per_device_train_batch_size 4
            --per_device_eval_batch_size 4
            --num_train_epochs 1
            --set_seq_size 8
            --encoder_model n-tokens
            --decoder_model n-tokens
            --n_latent_tokens 1
            --latent_size 2
            --transformer_critic_name funnel-transformer/intermediate
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
            self.assertAlmostEqual(result["epoch"], 1.0)

    def test_train_smooth(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --do_eval
            --eval_steps 3
            --evaluation_strategy steps
            --sample_from_latent
            --per_device_train_batch_size 4
            --per_device_eval_batch_size 4
            --num_train_epochs 1
            --set_seq_size 8
            --encoder_model n-tokens
            --decoder_model n-tokens
            --n_latent_tokens 1
            --latent_size 2
            --smooth_cosine
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
            self.assertAlmostEqual(result["epoch"], 1.0)

    def test_train_cycle_loss(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --do_eval
            --eval_steps 3
            --evaluation_strategy steps
            --sample_from_latent
            --per_device_train_batch_size 4
            --per_device_eval_batch_size 4
            --num_train_epochs 1
            --set_seq_size 8
            --encoder_model n-tokens
            --decoder_model n-tokens
            --n_latent_tokens 1
            --latent_size 2
            --cycle_loss
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
            self.assertAlmostEqual(result["epoch"], 1.0)

    def test_train_mini_mmd_batch_size(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --do_eval
            --eval_steps 3
            --evaluation_strategy steps
            --sample_from_latent
            --per_device_train_batch_size 4
            --per_device_eval_batch_size 4
            --mmd_batch_size 2
            --num_train_epochs 1
            --set_seq_size 8
            --encoder_model n-tokens
            --decoder_model n-tokens
            --n_latent_tokens 1
            --latent_size 2
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
            self.assertAlmostEqual(result["epoch"], 1.0)

    def test_interpolate_training_step_rate(self):
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)

        tmp_dir = self.get_auto_remove_tmp_dir()
        testargs = f"""
            train.py
            --train_file ./tests/fixtures/line_by_line_max_len_3.txt
            --validation_file ./tests/fixtures/line_by_line_max_len_3.txt
            --do_train
            --do_eval
            --eval_steps 3
            --evaluation_strategy steps
            --sample_from_latent
            --per_device_train_batch_size 4
            --per_device_eval_batch_size 4
            --interpolate_training_step_rate 2
            --cycle_loss
            --transformer_critic_name funnel-transformer/intermediate
            --num_train_epochs 1
            --set_seq_size 8
            --min_critic_steps 1
            --encoder_model n-tokens
            --decoder_model n-tokens
            --n_latent_tokens 1
            --latent_size 2
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
            self.assertAlmostEqual(result["epoch"], 1.0)
