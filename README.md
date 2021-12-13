# group-of-pictures
A python/flask/ffmpeg API to display/slice an MP4 along GOP i-frame boundaries

## Overview
This is a small API that can pull GOP video data and metadata out of a video file. It assumes the video file is stored locally on the filesystem of the web server.

### New / Interesting Concepts
I work primarily in Spring Boot when creating API's. The concept of a `blueprint` within the Flask framework is new to me. It seems like a powerful construct, and allows you to separate the HTTP aspects of your controllers from the view formatting done within a controller. if I were to create a larger API using python and Flask I would want to lean into this and other concepts or patterns that the Flask project recommends.
### Design Decisions
The code has been structured so that response codes and content formatting are done within the controller module, while the engine module contains the interface to the external `ffprobe`/`ffmpeg` programs.

This is my first time working with `flask` in quite some time. I have tried to follow generic MVC and API best practices, as well as flask-specific best practices, as much as possible within a project of such a small size, and without polluting the code with too many unnecessary abstractions.
### Flexibility
By structuring the project into a controller module and an engine module, I have hopefully made it easier to use a different video processing engine, if needed. Additionally, adding endpoints or changing the display layout of existing endpoints should be easier to accomplish with this separation, without needing to modify the underlying video processing code.

The ffprobe and ffmpeg commands and arguments used by the engine module are currently hard-coded. Extracting these into default values, or using some additional configuration file, should make the code more flexible if different options are needed.
### Performance bottlenecks
* The fact that the GOP video segments and metadata are not persisted between subsequent requests is an inherent performance bottleneck, as the web server must reprocess the source video file again for every API request.
* At a minimum, we may want to cache the frame metadata from the video after the first request for any video processing of a video. This would reduce the processing time for subsequent calls to only require the time it takes to slice and return a portion of the video stream.
* We may also wish to cache each GOP video locally on the web server, if the service would be used heavily. We would want to examine storage constraints and possibly institute some sort of cache expiry for these larger files to avoid unexpected failures from too many intermediate files impacting the operation of the web server.
## Setup
### Requirements
* `python3` -- This API was built and tested using python 3.9.6, but any recent version of python3 should work.
* `pip` module in `python3`
* `ffprobe` and `ffmpeg` executables within the `$PATH` of the user running the `flask` web server process

You can use python's pip module to install the flask web server module in your python environment:
* `python3 -m pip install -r requirements.txt`

## Execution
Start the web server by running the following command in the `src` directory of this repository:
```flask run```

Please note that the API will only process video files that are located at the top level within the `src` directory within the repository.

Also, please note that in my testing, flask only exposed the webserver at the `http://127.0.0.1:5000/` address. Attempting to access `http://localhost:5000/` may return a `403` unauthorized response.

## Endpoints
### /videos/{video-filename}/group-of-pictures.json
Returns the detail for the i-frames within the video, encoded in JSON format.
### /videos/{video-filename}/group-of-pictures/{gop-index}.mp4
Returns an mp4 file containing only the video data for the group of pictures requested. This endpoint is zero-indexed.
### /videos/{video-filename}/group-of-pictures
Returns an HTML document that contains a grid of all of the groups of pictures within the video.

## Testing
This API was tested manually using a web browser and a sample video file.

Unit tests should be added for the controller and engine modules.

## Future Enhancements
### Dynamically cropping or filtering videos with a query string
`ffmpeg` supports a number of [video filters](https://ffmpeg.org/ffmpeg-filters.html). If filters such as cropping or monotone color conversion are already supported by `ffmpeg`, we should be able to add support for those or any other specific video transformation with two changes within the codebase:
* Controller module
  * Parse the filter arguments from the query parameters
  * Send the filter information to the engine module
* Engine module
  * Convert incoming filter information into arguments/formatting that `ffmpeg` understands
    * Please see the above [video filters](https://ffmpeg.org/ffmpeg-filters.html) page for specific info about the available video filters and the required arguments/formatting.
  * Add the `ffmpeg`-compatible filter arguments when calling `ffmpeg`

## Additional Notes
While I already had a passing familiarity with Python 3's subprocess module, I also relied on the following gist for getting the frame information in json format from ffprobe:

[iframe-probe.py](https://gist.github.com/alastairmccormack/7041ee993adb5c911f90)

I followed this blog entry for structuring the flask controller/blueprint so that I could separate the ffmpeg-interfacing bits into the engine module.

[Building a Flask CRUD Application with MVC Architecture](https://python.plainenglish.io/flask-crud-application-using-mvc-architecture-3b073271274f)

I also used various stack overflow pages and google searches to learn about ffmpeg seeking and video file manipulation.