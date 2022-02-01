
import json

class Profile:
    scales = {"720p": "-1:720", "1080p": "-1:1080"}

    def __init__(self, profile):
        self.profile = profile

    def build_params(self):
        bitrate = self.profile["bitrate"]
        br_multiple = self.profile["br_variable"] / 100

        params = ["-vf", "scale={scale}".format(scale=self.scales[self.profile["size"]]),
            "-c:v", "{codec}".format(**self.profile),
            "-b:v", "{bitrate}k".format(bitrate=bitrate),
            "-maxrate", "{maxrate}k".format(maxrate=bitrate*br_multiple),
            "-bufsize", "{bufsize}k".format(bufsize=bitrate*br_multiple),
            "-profile:v", "{profile_name}".format(**self.profile),
            "-x264-params", "bframes={bframes}".format(**self.profile),
            "-c:a", "copy"]

        return params

    def build_output_file_name(self):
        br_variable = self.profile["br_variable"]
        if br_variable > 100:
            br_mode = '{percent}BR'.format(percent=br_variable)
        else:
            br_mode = 'CBR'
        output_file_name = '{codec}_{size}_{bitrate}k_{profile_name}_bf{bframes}_{br_mode}'.format(**self.profile,br_mode=br_mode)
        return output_file_name


class Configuration:
    def __init__(self, ffmpeg_tools, hwaccel, output_dir, profiles, metrics):
        self.ffmpeg_tools = ffmpeg_tools
        self.hwaccel = hwaccel
        self.output_dir = output_dir
        self.profiles = []
        for item in profiles:
            self.profiles.append(Profile(item))
        self.metrics = metrics

def prepare_config(args):
    with open(args.config) as json_file:
        data = json.load(json_file)
        config = Configuration(**data)
        print(config.output_dir)
    
    return config