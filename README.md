# Video-quality-analyzer
Transcoding and qualitative video analysis program

## Start program
`py video_analyzer.py -i origin_video.mp4`

`py video_analyzer.py -i origin_video.mp4 -c custom_config.json`

## Сonfig parameters
ffmpeg_tools - the path to ffmpeg tools

hwaccel - hw decode

output_dir - the path to save results

profiles - transcoding profiles 

metrics - supported metrics

## Profile parameters
codec - codec name (h264, libx264)

size - scale parameter

bitrate - transcode bitrate 2500

profile_name - main, baseline

bframes - buffer frames

br_variable - bitrate variable in percent(if 100% then cbr)

## Example
```
{
    "ffmpeg_tools" : "/path/to/ffmpeg/tools",
    "hwaccel": "dxva2",
    "output_dir": "./output",
    "profiles": [
        {
            "codec": "h264",
            "size": "1080p",
            "bitrate": 2500,
            "profile_name": "main",
            "bframes": 0,
            "br_variable": 100
        }
    ],
    "metrics": [
        "PSNR"
    ]
}
```
