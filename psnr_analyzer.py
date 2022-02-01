import subprocess

def get_hwdevice(hwaccel):
    if hwaccel == "none":
        return ""
    else:
        return hwaccel

class PsnrAnalyzer:
    def __init__(self, ffmpeg_tools, hwaccel, output_dir):
        self.ffmpeg_program = ffmpeg_tools + '/ffmpeg'
        self.hwaccel = hwaccel
        self.output_dir = output_dir

    def analyze(self, transcode_file, origin_file, pnsr_report_name):
        outputFile = self.output_dir + "/" + pnsr_report_name + ".log"
        print("Start pnsr analyze")
        print('Transcode file: {outputFile}'.format(outputFile=transcode_file))
        print('Origin file: {outputFile}'.format(outputFile=origin_file))
        print('Report file: {outputFile}'.format(outputFile=outputFile))

        call_params = [self.ffmpeg_program]
        hwaccels = get_hwdevice(self.hwaccel)
        if(hwaccels):
            call_params.append("-hwaccel")
            call_params.append(hwaccels)
        call_params.extend(["-i", transcode_file])
        call_params.extend(["-i", origin_file])
        call_params.extend([
            "-filter_complex",
            '[0:v]scale=1920x1080:flags=bicubic[main];[1:v]scale=1920x1080:flags=bicubic[ref];[main][ref]psnr={outputFile}'.format(outputFile=outputFile)])
        # call_params.extend(["-lavfi", 'psnr=stats_file={outputFile}'.format(outputFile=outputFile)])
        call_params.extend(["-f", "null"])
        call_params.append("-")

        print("Wait...")
        
        subprocess.call(call_params, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("End analyze")

        return outputFile