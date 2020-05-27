import subprocess
import shlex
import os 

# Notes: This is the setup used to get the 5 folds of the rotnet for our evaluation of rotation predictions

# TODO: you will want to change this to your checkpoint filepath. 
checkpoint_fp = '/userdata/smetzger/all_deepul_files/ckpts'

# Imagenet pretrain
for fold in range(5):

    # This is all code for my queue system, basically just submits it and writes the output to a txt file. 
    filename = '/userdata/smetzger/all_deepul_files/runs/imgnet_fold%d.txt' %(fold)
    string = "submit_job -q mind-gpu"
    string += " -m 318 -g 4"
    string += " -o " + filename
    string += ' -n inet_moco'
    string += ' -x python /userdata/smetzger/all_deepul_files/deepul_proj/moco/main_moco.py'

    # add all the default args: 
    string += " -a resnet50 --lr 0.015  --batch-size 128 --dist-url 'tcp://localhost:10001' --multiprocessing-distributed --world-size 1"
    string += ' --moco-t 0.2' # MoCov2 arguments. 
    string += ' --checkpoint_fp ' + str(checkpoint_fp)
    string += ' --rank 0'
    string += " --data /PATH/TO/IMAGENET "
    string += " --notes 'YOURNOTESHERE'"
    string += ' --dataid imagenet'
    string += ' --reduced_imgnet'# reduced imagenet. WE train our initial runs with only 50k of the examples.
                                    # This makes FAA go faster, and reduces overhead. 
    string += ' --mlp --cos --epochs 500' # because we have the reduced dataset, we run for 500 epochs
    string += ' --aug-plus'
    string += ' --kfold %d' %fold

    cmd = shlex.split(string)
    print(cmd)
    subprocess.run(cmd, stderr=subprocess.STDOUT)

# SVHN pretrain
for fold in range(5):

    # This is all code for my queue system, basically just submits it and writes the output to a txt file. 
    filename = '/userdata/smetzger/all_deepul_files/runs/svhn_fold%d.txt' %(fold)
    string = "submit_job -q mind-gpu"
    string += " -m 318 -g 4"
    string += " -o " + filename
    string += ' -n inet_moco'
    string += ' -x python /userdata/smetzger/all_deepul_files/deepul_proj/moco/main_moco.py'

    # add all the default args for SVHN.
    string += " -a resnet50 --lr 0.4  --batch-size 512 --dist-url 'tcp://localhost:10001' --multiprocessing-distributed --world-size 1"
    string += ' --moco-t 0.2' # MoCov2 arguments. 
    string += ' --checkpoint_fp ' + str(checkpoint_fp)
    string += ' --rank 0'
    string += " --data /PATH/TO/SVHN"
    string += " --notes 'YOURNOTESHERE'"
    string += ' --dataid svhn'
    string += ' --mlp --cos --epochs 750' # we pretrain for 750 epochs.
    string += ' --aug-plus'
    string += ' --kfold %d' %fold

    cmd = shlex.split(string)
    print(cmd)
    subprocess.run(cmd, stderr=subprocess.STDOUT)