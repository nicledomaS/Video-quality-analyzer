import re
import numpy as np

def average(lst):
    return sum(lst) / len(lst)

class PsnrReport:
    def __init__(self, workbook, common_worksheet, avg_index, bad_index):
        self.workbook = workbook
        self.common_worksheet = common_worksheet
        self.avg_index = avg_index
        self.bad_index = bad_index
        self.worksheet = self.workbook.add_worksheet("PSNR")
        self.index = 0

        self.chart = self.workbook.add_chart({'type': 'line'})
        self.chart.set_y_axis({'name': 'PSNR_AVG'})
        self.chart.set_x_axis({'name': 'Frame number'})
        self.chart.set_title({'name': 'Psnr by transcode file'})
        self.worksheet.insert_chart('K1', self.chart)

    def add_report_by_file(self, report_data):

        data = []
        with open(report_data.log_files["PSNR"], "r") as f:
            for line in f.readlines():
                row = dict([s.split(':') for s in re.findall('[\S]+:[\S]+', line)])
                data.append(row["psnr_avg"])
                    
        numpy_array = np.array(data).astype(np.float)
        psnr_array = numpy_array[np.isfinite(numpy_array)]
        
        self.common_worksheet.write(report_data.row_id, self.avg_index, average(psnr_array))
        self.common_worksheet.write(report_data.row_id, self.bad_index, min(psnr_array))

        self.worksheet.write(0, self.index, report_data.transcode_file_name)

        self.worksheet.write_column(1, self.index, numpy_array)

        self.chart.add_series({
            'values': ["PSNR", 1, self.index, len(data) + 1, self.index],
            'name': "{0}".format(report_data.transcode_file_name),
        })

        self.index += 1