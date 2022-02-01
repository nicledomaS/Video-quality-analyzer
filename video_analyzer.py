#!/usr/bin/python

import glob
import argparse
import os
import sys
from psnr_analyzer import PsnrAnalyzer

from report_manager import ReportData, ReportManager

from transcoder import Transcoder
from configuration import prepare_config

def prepare_output_dir(output_dir):
        if os.path.exists(output_dir):
            print("Clear output folder")
            filelist = glob.glob(os.path.join(output_dir, "*"))
            for file in filelist:
                print("Remove: " + file)
                os.remove(file)
        else:
            print("Create output folder")
            os.mkdir(output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ping script")

    parser.add_argument("-i", dest="input", help="Origin input file", required=True)
    parser.add_argument("-c", dest="config", help="Config file", default="config.json", required=False)

    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
        sys.exit()

    original_file_size = os.path.getsize(args.input)
    config = prepare_config(args)

    prepare_output_dir(config.output_dir)

    analyzers = { "PSNR": PsnrAnalyzer(config.ffmpeg_tools, config.hwaccel, config.output_dir) }
    transcoder = Transcoder(config.ffmpeg_tools, config.hwaccel, config.output_dir)
    report_manager = ReportManager(config.output_dir)

    row_id = 1
    report_datas = []

    for profile in config.profiles:
        transcode_file_path = transcoder.transcode(args.input, profile)
        transcode_file_size = os.path.getsize(transcode_file_path)
        difference_in_percent = 100 - (transcode_file_size / original_file_size) * 100
        report_data = ReportData(row_id, transcode_file_path, profile.build_output_file_name(), transcode_file_size, difference_in_percent)
        report_datas.append(report_data)
        row_id += 1

    for report_data in report_datas:
        for item in config.metrics:
            log_file = analyzers[item].analyze(report_data.transcode_file_path, args.input, report_data.transcode_file_name)
            report_data.add_report(item, log_file)

    for report_data in report_datas:
        report_manager.add_report(report_data)

