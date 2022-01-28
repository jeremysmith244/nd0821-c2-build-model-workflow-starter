#!/usr/bin/env python
"""
Download raw dataDownload raw data from W&b, transform columns to proper types, filter price
"""
import argparse
import logging

from gevent import config
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################

    logger.info("Downloading raw data artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path, index_col="id")

    logger.info("Processing raw data artifact")
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    df.to_csv(args.output_artifact)

    logger.info("Creating clean artifact")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(args.output_artifact)

    logger.info("Logging artifact")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Simple data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of W&B artifact to be be cleaned",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of cleaned artifact to upload to W&B",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Artifact type for ouput",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Min price filter to apply to price column",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Max price filter to apply to price column",
        required=True
    )


    args = parser.parse_args()

    go(args)
