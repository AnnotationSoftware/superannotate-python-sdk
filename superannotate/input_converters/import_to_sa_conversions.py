"""
Module which will run converters and convert from other 
annotation formats to superannotate annotation format
"""
import sys
import os
import glob
import shutil
import logging
from argparse import Namespace

from .converters.converters import Converter


def _load_files(path_to_imgs, ptype):
    images = glob.glob(
        os.path.join(path_to_imgs, "**", "*.jpg"), recursive=True
    )
    if not images:
        logging.warning("Images doesn't exist")

    if ptype == "Pixel":
        masks = glob.glob(
            os.path.join(path_to_imgs, "**", "*.png"), recursive=True
        )
        if not masks:
            logging.warning("Masks doesn't exist")
    else:
        masks = None

    return images, masks


def _move_files(imgs, masks, output_dir, platforom):
    if platforom == "Desktop":
        output_path = os.path.join(output_dir, "images")
        os.makedirs(output_path)
    else:
        output_path = output_dir

    if imgs is not None:
        for im in imgs:
            shutil.copy(im, os.path.join(output_path, os.path.basename(im)))

    if masks is not None:
        for mask in masks:
            shutil.copy(mask, os.path.join(output_path, os.path.basename(mask)))


def import_to_sa(args):
    """
    :param args: All arguments that will be used during convertion.
    :type args: Namespace
    """
    try:
        os.makedirs(os.path.join(args.output_dir, "classes"))
    except Exception as e:
        logging.error(
            "Could not create output folders, check if they already exist"
        )
        sys.exit()

    try:
        images, masks = _load_files(args.input_dir, args.project_type)
    except Exception as e:
        logging.error("Can't load images or masks")
        logging.error(e)

    try:
        _move_files(images, masks, args.output_dir, args.platform)
    except Exception as e:
        logging.error(
            'Something is went wrong while moving or copying files from source folder'
        )
        logging.error(e)

    method = Namespace(
        direction="from",
        dataset_format=args.dataset_format,
    )

    converter = Converter(
        args.project_type, args.task, args.dataset_name, args.input_dir,
        args.output_dir, method
    )

    try:
        converter.convert_to_sa(args.platform)
    except Exception as e:
        logging.error("Something went wrong while converting")
        sys.exit()

    logging.info('Conversion completed successfully')
