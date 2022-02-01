import subprocess

def get_hwdevice(hwaccel):
    if hwaccel == "none":
        return ""
    else:
        return hwaccel

class Transcoder:
    def __init__(self, ffmpeg_tools, hwaccel, output_dir):
        self.ffmpeg_program = ffmpeg_tools + '/ffmpeg'
        self.hwaccel = hwaccel
        self.output_dir = output_dir
    
    def transcode(self, inputFile, profile):
        outputFile = self.output_dir + "/" + profile.build_output_file_name() + ".mp4"
        print("Start transcode")
        print('Output file: {outputFile}'.format(outputFile=outputFile))

        call_params = [self.ffmpeg_program]
        hwaccels = get_hwdevice(self.hwaccel)
        if(hwaccels):
            call_params.append("-hwaccel")
            call_params.append(hwaccels)
        call_params.extend(["-i", inputFile])

        params = profile.build_params()
        call_params.extend(params)
        call_params.append(outputFile)

        print("Wait...")

        subprocess.call(call_params, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("End transcode")

        return outputFile
