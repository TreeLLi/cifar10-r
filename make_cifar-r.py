'''
This script is adapted from the code of paper: A Downsampled Variant of ImageNet as an Alternative to the CIFAR datasets.

The original source code repository is: https://github.com/PatrykChrabaszcz/Imagenet32_Scripts


'''

import os, shutil
from PIL import Image
from argparse import ArgumentParser
from multiprocessing import Pool

alg_dict = {
    'lanczos': Image.LANCZOS,
    'nearest': Image.NEAREST,
    'bilinear': Image.BILINEAR,
    'bicubic': Image.BICUBIC,
    'hamming': Image.HAMMING,
    'box': Image.BOX
}

def str2alg(str):
    str = str.lower()
    return alg_dict.get(str, None)

# Takes in_dir, out_dir and alg as strings
# resize images from in_dir using algorithm deduced from
# alg string and puts them to "out_dir/alg/" folder
def resize_img_folder(in_dir, out_dir, alg):
    print('Folder %s' % in_dir)

    alg_val = str2alg(alg)

    if alg_val is None:
        print("Sorry but this algorithm (%s) is not available, use help for more info." % alg)
        return

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for filename in os.listdir(in_dir):
        # Exception raised when file is not an image
        try:
            im = Image.open(os.path.join(in_dir, filename))

            # Convert grayscale images into 3 channels
            if im.mode != "RGB":
                im = im.convert(mode="RGB")

            im_resized = im.resize((size, size), alg_val)
            # Get rid of extension (.jpg or other)
            filename = os.path.splitext(filename)[0]
            im_resized.save(os.path.join(out_dir, filename + '.png'))
        except OSError as err:
            print("This file couldn't be read as an image")
            with open("log.txt", "a") as f:
                f.write("Couldn't resize: %s" % os.path.join(in_dir, filename))


if __name__ == '__main__':
    in_dir = 'data/cifar-10-r_'
    out_dir = 'data/cifar-10-r'    
    alg = 'box'
    size = 32
    processes = 16
    
    print('Starting ...')

    pool = Pool(processes=processes)

    print('Using algorithm %s ...' % alg)
    print('Recurrent for all folders in in_dir:\n %s' % in_dir)
    folders = [dir for dir in sorted(os.listdir(in_dir)) if os.path.isdir(os.path.join(in_dir, dir))]
    for i, folder in enumerate(folders):
        r = pool.apply_async(
            func=resize_img_folder,
            args=[os.path.join(in_dir, folder), os.path.join(out_dir, folder), alg])
    pool.close()
    pool.join()
    print("Finished.")
