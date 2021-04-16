from __future__ import print_function

import configparser
import os
import sys
import time

from gapi import build_gapi_service
from pipeline import Pipeline
from uploader import Uploader
from processMetaData import MetaDataProcessor


# Global Objects


def job_summary(config):
    template = """
    ======================================
                  JOB SUMMARY
    ======================================
    Script Version: {}
    
    ---------- Input Information ---------
    Input Data Folder: {}
    Log Type: {}
    Nodes: {}
    ChunkSize: {}
    
    -------- Output Information  ---------
    MakeChunk: {}
    Upload: {}
    UploadFolder: {}
    
    ------ Google Drive Information ------
    ParentFolder: {}
    ParentFolderID: {}
    ======================================
    """

    print(template.format(
        config['Version'].get("Number"),
        config["Input"].get("DataFolder"),
        config["Input"].get("Type"),
        config["Input"].get("Nodes"),
        config["Input"].get("PartitionSize"),
        config["Output"].get("MakeChunk"),
        config["Output"].get("Upload"),
        config["Output"].get("UploadFolder"),
        config["GoogleDrive"].get("ParentFolder"),
        config["GoogleDrive"].get("ParentFolderID")
    ))

    return (
        config['Version'].get("Number"),
        config["Input"].get("DataFolder"),
        config["Input"].get("Type").split(","),
        config["Input"].get("Nodes").split(","),
        config["Input"].get("PartitionSize"),
        True if (config["Output"].get("MakeChunk")) == "True" else False,
        True if (config["Output"].get("Upload") == "True") else False,
        (config["GoogleDrive"].get("ParentFolder"), config["GoogleDrive"].get("ParentFolderID"))
    )


def main():
    # read configuration file
    config = configparser.ConfigParser()
    config.read('app.ini')
    _, data_path, types, nodes, size, make_chunk, upload, google_directory_id = job_summary(config)

    if make_chunk:
        for log_type in types:
            if log_type != 'sent' and log_type != 'trace':
                print("invalid log type! it should be either sent or trace", file=sys.stderr)
                exit(1)

            # create output directory
            output_folder = "../output/{}_{}_{:d}/".format(log_type, "-".join(nodes), int(time.time()))

            nodes_int = map(int, nodes)

            try:
                os.makedirs(output_folder, exist_ok=True)
                print("Output Folder: {}".format(output_folder))
            except FileExistsError as e:
                print(e, file=sys.stderr)
                exit(1)

            pipe = Pipeline(log_type, nodes_int, output_folder)
            pipe.process_all_log()

    if upload:
        service = build_gapi_service()
        folder = config["Output"].get("UploadFolder")
        uploader = Uploader(service, folder, google_directory_id)
        meta_path = uploader.start()
        processor = MetaDataProcessor(meta_path)
        processor.process()


if __name__ == "__main__":
    main()
