# Bidirectional-PDP
This bidirectional Parallel Distributed Processing (PDP) network was trained with either an orthography-phonology or phonology-orthography mapping task, corresponding to reading aloud visually presented words, and spelling spoken words, respectively. Our focus is on the PDP framework developed by \citeA{rumelhart1986general} that provides natural accounts of the exploitation of multiple, simultaneous, and often mutual constraints. To examine the ease with which the model can generate the target output for a word, we measured the closeness of the model's output to the target by calculating the mean squared error (MSE) that serves as a reflection of how difficult it was for the model to learn the GPC/PGC mappings of each word. 

# Paper
![architecture](architecture.png)
<img src="architecture.png" width="48">

# Paper
This repo implements our paper:

Lim, O'Brien, & Onnis (submitted), “[Orthography-phonology consistency in English: Theory- and data-driven measures and their impact on auditory vs. visual word recognition](https://osf.io/wdzqc/?view_only=d6ef4592811441779ce7e8801dec805d),” in [journal to be confirmed].

Please cite our paper if the code is useful for your project.
```
@article{TBD,
  title={Orthography-phonology consistency in English: Theory- and data-driven measures and their impact on auditory vs. visual word recognition},
  author={TBD},
  journal={TBD},
  volume={TBD},
  number={TBD},
  pages={TBD},
  year={TBD},
  publisher={TBD}
}

```
You may also find our [OSF repository](https://osf.io/wdzqc/?view_only=d6ef4592811441779ce7e8801dec805d) useful.

# Hints for First-Time Users
Note that following the data structure of our [DACT](https://github.com/yining043/VRP-DACT), we use linked list to store solutions. We thus highly recommend you to read our Jupyter notebook for DACT before getting into details of our code for N2S. Please open the [Jupyter notebook](https://github.com/yining043/VRP-DACT/blob/main/Play_with_DACT.ipynb) here :)

Meanwhile, a refactoring of this repo can be found in branch [refactor](https://github.com/yining043/PDP-N2S/tree/refactor), where the names of variables are changed to be consistent with the paper, some minor bugs are fixed, and the type hints for python are provided, which is supposed to be more convenient for the first-time user of the project. We thank [@ci-ke](https://github.com/ci-ke) for the nice refactoring.


# Dependencies
* Python>=3.8
* PyTorch>=1.7
* numpy
* tensorboard_logger
* tqdm

# Usage
## Generating data
Training data is generated on the fly. Please follow repo [Demon0312/Heterogeneous-Attentions-PDP-DRL](https://github.com/Demon0312/Heterogeneous-Attentions-PDP-DRL) to generate validating or test data if needed. We also provide some randomly generated data in the  [datasets](./datasets) folder.

## Training
### PDTSP examples
20 nodes:
```python
CUDA_VISIBLE_DEVICES=0 python run.py --problem pdtsp --graph_size 20 --warm_up 2 --max_grad_norm 0.05 --val_m 1 --val_dataset './datasets/pdp_20.pkl' --run_name 'example_training_PDTSP20'
```

50 nodes:
```python
CUDA_VISIBLE_DEVICES=0,1 python run.py --problem pdtsp --graph_size 50 --warm_up 1.5 --max_grad_norm 0.15 --val_m 1 --val_dataset './datasets/pdp_50.pkl' --run_name 'example_training_PDTSP50'
```

100 nodes:
```python
CUDA_VISIBLE_DEVICES=0,1,2,3 python run.py --problem pdtsp --graph_size 100 --warm_up 1 --max_grad_norm 0.3 --val_m 1 --val_dataset './datasets/pdp_100.pkl' --run_name 'example_training_PDTSP100'
```
### PDTSP-LIFO examples
20 nodes:
```python
CUDA_VISIBLE_DEVICES=0 python run.py --problem pdtspl --graph_size 20 --warm_up 2 --max_grad_norm 0.05 --val_m 1 --val_dataset './datasets/pdp_20.pkl' --run_name 'example_training_PDTSPL20'
```

50 nodes:
```python
CUDA_VISIBLE_DEVICES=0,1 python run.py --problem pdtspl --graph_size 50 --warm_up 1.5 --max_grad_norm 0.15 --val_m 1 --val_dataset './datasets/pdp_50.pkl' --run_name 'example_training_PDTSPL50'
```

100 nodes:
```python
CUDA_VISIBLE_DEVICES=0,1,2,3 python run.py --problem pdtspl --graph_size 100 --warm_up 1 --max_grad_norm 0.3 --val_m 1 --val_dataset './datasets/pdp_100.pkl' --run_name 'example_training_PDTSPL100'
```

### Warm start
You can initialize a run using a pretrained model by adding the --load_path option:
```python
--load_path '{add model to load here}'
```
### Resume Training
You can resume a training by adding the --resume option:
```python
--resume '{add last saved checkpoint(model) to resume here}'
```
The Tensorboard logs will be saved to folder "logs" and the trained model (checkpoint) will be saved to folder "outputs". Pretrained models are provided in the [pre-trained](./pre-trained) folders.

## Inference
Load the model and specify the iteration T for inference (using --val_m for data augments):

```python
--eval_only 
--load_path '{add model to load here}'
--T_max 3000 
--val_size 2000 
--val_batch_size 200 
--val_dataset '{add dataset here}' 
--val_m 50
```

### Examples
For inference 2,000 PDTSP instances with 100 nodes and no data augment (N2S):
```python
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python run.py --eval_only --no_saving --no_tb --problem pdtsp --graph_size 100 --val_m 1 --val_dataset './datasets/pdp_100.pkl' --load_path 'pre-trained/pdtsp/100/epoch-195.pt' --val_size 2000 --val_batch_size 2000 --T_max 3000
```
For inference 2,000 PDTSP instances with 100 nodes using the augments in Algorithm 2 (N2S-A):
```python
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 python run.py --eval_only --no_saving --no_tb --problem pdtsp --graph_size 100 --val_m 50 --val_dataset './datasets/pdp_100.pkl' --load_path 'pre-trained/pdtsp/100/epoch-195.pt' --val_size 2000 --val_batch_size 200 --T_max 3000
```
See [options.py](./options.py) for detailed help on the meaning of each argument.

# Acknowledgements
The code and the framework are based on the repos [yining043/VRP-DACT](https://github.com/yining043/VRP-DACT).
