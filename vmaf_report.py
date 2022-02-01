class VmafReport:
    def __init__(self, workbook, common_worksheet, avg_index, bad_index):
        self.workbook = workbook
        self.worksheet = self.workbook.add_worksheet("VMAF")
        self.index = 0

    def add_report_by_file(self, report_data):
        print("Not implemented")
        # todo: implementation