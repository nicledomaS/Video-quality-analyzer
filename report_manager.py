import os
import re
import xlsxwriter

from psnr_report import PsnrReport
from vmaf_phone_report import VmafPhoneReport
from vmaf_report import VmafReport

class ReportData:
    def __init__(self, row_id, transcode_file_path, transcode_file_name, transcode_file_size, difference_in_percent):
        self.row_id = row_id
        self.transcode_file_path = transcode_file_path
        self.transcode_file_name = transcode_file_name
        self.transcode_file_size = transcode_file_size
        self.difference_in_percent = difference_in_percent
        self.log_files = {}
    
    def add_report(self, metric_type, log_file):
        self.log_files[metric_type] = log_file

class ReportManager:
    column_names = ["File name", "Size", "Diff in %", "Psnr avg", "The worst psrn", "Vmaf avg", "The worst vmaf", "Vmaf_phone avg", "The worst vmaf_phone"]

    def __init__(self, output_dir):
        self.workbook = xlsxwriter.Workbook(output_dir + "/report.xlsx", {'nan_inf_to_errors': True})
        self.worksheet = self.workbook.add_worksheet("Common")
        alfa = 0
        for column_name in self.column_names:
            self.worksheet.write(0, alfa, column_name)
            alfa += 1
        
        self.report_builders = {}
        self.report_builders["PSNR"] = PsnrReport(self.workbook, self.worksheet, 3, 4)
        self.report_builders["VMAF"] = VmafReport(self.workbook, self.worksheet, 5, 6)
        self.report_builders["VMAF_phone"] = VmafPhoneReport(self.workbook, self.worksheet, 7, 8)

    def __del__(self):
        self.workbook.close()

    def add_report(self, report_data):
        for metric_type in report_data.log_files.keys():
            if metric_type in self.report_builders:
                self.worksheet.write(report_data.row_id, 0, report_data.transcode_file_name)
                self.worksheet.write(report_data.row_id, 1, report_data.transcode_file_size)
                self.worksheet.write(report_data.row_id, 2, report_data.difference_in_percent)

                self.report_builders[metric_type].add_report_by_file(report_data)

        
        