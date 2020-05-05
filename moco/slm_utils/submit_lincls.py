print('Sko Buffs')
import subprocess
import shlex
import os 

base_model_name = ''
epochs = 750
import os

def find_model(name, fold, epochs, basepath="/userdata/smetzger/all_deepul_files/ckpts"):
    """
    name = model name
    fold = which fold of the data to find. 
    epochs = how many epochs to load the checkpoint at (e.g. 750)
    
    """
    for file in os.listdir(basepath):
        if name in str(file) and 'fold_%d' %fold in str(file):
            if str(file).endswith(str(epochs-1) + '.tar'): 
                return os.path.join(basepath, file)
            
    print("COULDNT FIND MODEL")
    assert True==False # just throw and error. 

base_name = 'resnet50_750epochs_512bsz_0.4000lr_0.9000mtm_120-160sched_128.0000mocod_65536mocok_0.9990mocom_0.2000mocot_1.000e-04wd_mlp_augplus_cos'
checkpoint_fp = '/userdata/smetzger/all_deepul_files/ckpts'


filename = '/userdata/smetzger/all_deepul_files/runs/lincls_moco_rot_top1_valid.txt'
string = "submit_job -q mind-gpu"
string += " -m 318 -g 4"
string += " -o " + filename
string += ' -n kf_lincls'
string += ' -x python /userdata/smetzger/all_deepul_files/deepul_proj/moco/main_lincls.py'

# add all the default args: 
string += " -a resnet50 --lr 15.0  --batch-size 256 --dist-url 'tcp://localhost:10001' --multiprocessing-distributed --world-size 1"
string += ' --checkpoint_fp ' + str(checkpoint_fp)
string += ' --rank 0'
string += ' --pretrained /userdata/smetzger/all_deepul_files/ckpts/GQw6A_2000epochs_512bsz_0.4000lr_mlp_cos_custom_aug_moco_rotation_top1_0749.tar'
string += " --data /userdata/smetzger/data/cifar_10/ --notes 'faa_top1_valid_rot_as_feedback'"
cmd = shlex.split(string)
print(cmd)
subprocess.run(cmd, stderr=subprocess.STDOUT)