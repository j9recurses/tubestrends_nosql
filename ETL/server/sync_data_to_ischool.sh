#!/bin/bash
#syncs combined daily data to the ischool

rsync -rtavz /mnt/s3/tubes_trends_orig/combined_data_json/ j9.heiser@ischool.berkeley.edu:/home/j9.heiser/tubes_trends_data/

