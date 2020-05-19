#!/bin/bash

PORT=$(( ( RANDOM % 60000 )  + 1025 ))

PERCENT=5

while read line
do
    echo "$line"

    echo "Starting run with prefix $line"
    # CIFAR 
    python main_lincls.py -a resnet50 --lr 15.0 --batch-size 256 --dist-url "tcp://localhost:${PORT}" --world-size 1 --rank 0 --pretrained $PWD/checkpoints/randaug/${line}*0499.tar --data /rscratch/data --dataid cifar10 --epochs 50 --schedule 10 20 --percent ${PERCENT} --loss-prefix "${PERCENT}percent"
done < "${1:-/dev/stdin}"

# for arg; do


# done
