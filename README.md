# Bidirectional-PDP
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

# Background
This bidirectional Parallel Distributed Processing (PDP) network was trained with either an orthography-phonology or phonology-orthography mapping task, corresponding to reading aloud visually presented words, and spelling spoken words, respectively. Our focus is on the PDP framework developed by [Rumelhart, Hinton, & McClelland (1986)](https://doi.org/10.7551/mitpress/5236.003.0018) that provides natural accounts of the exploitation of multiple, simultaneous, and often mutual constraints. To examine the ease with which the model can generate the target output for a word, we measured the closeness of the model's output to the target by calculating the mean squared error (MSE) that serves as a reflection of how difficult it was for the model to learn the GPC/PGC mappings of each word. 

# Architecture
<img src="architecture.png" width="500">

# Hints for First-Time Users
Acquire Lens from either: (1) [the main site](https://www.cnbc.cmu.edu/~plaut/Resources.html); (2) [Plaut's lab website](https://www.cnbc.cmu.edu/~plaut/Resources.html); or (3) [our backup repository](https://github.com/alfred-lim/Lens). In order to run a simulation, put a model file (e.g., model_reading.tcl), and a training testing examples file (e.g., OP.txt; see ./dictionary for definition of phonological representations of phonemes), and training and testing examples (Tr#.txt and Te#.txt, see ./dictionary for the examples following the two types of phonological representations) into the same directory.

## Required files
* Model file (e.g., model_reading.tcl, model_spelling.tcl)
* Data file (e.g., OP.ex, PO.ex)

# Usage
The model implements a multi-layer neural network from orthography to phonology. The model can be trained in two aspects: training the mapping from orthography to phonology (OP) and training the mapping from phonology to orthography (PO).

## Training data
Training data is selected from the example file (e.g., OP.ex) on the fly.

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
