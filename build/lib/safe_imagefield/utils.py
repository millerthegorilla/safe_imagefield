import ffmpeg, logging, math, magic, PIL

# some of the below code is from https://github.com/ftarlao/check-media-integrity
# there,the author recommends uninstalling pillow and installing pillow-simd in its place
# pillow-simd requires that you have a processor that supports MMX, SSE-SSE4, AVX, AVX2, AVX512, NEON
# or similar

logger = logging.getLogger('safe_imagefield')

def detect_content_type(f) -> str:
    sample = f.read(2048)
    f.seek(0)
    return magic.from_buffer(sample, mime=True)

def ffmpeg_check(filename, error_detect='default', threads=0) -> None:
    try:
        if error_detect == 'default':
            stream = ffmpeg.input(filename)
        else:
            if error_detect == 'strict':
                custom = '+crccheck+bitstream+buffer+explode'
            else:
                custom = error_detect
            stream = ffmpeg.input(
                filename, **{'err_detect': custom, 'threads': threads})

        stream = stream.output('pipe:', format="null")
        stream.run(capture_stdout=True, capture_stderr=True)
    except Exception as e:
        logger.info('error when checking ffmpeg')


def pil_check(file) -> None:
    # Image manipulation is mandatory to detect few defects
    # detects truncated file.
    img = PIL.Image.open(file)
    img.transpose(PIL.Image.FLIP_LEFT_RIGHT)


def convert_size(size_bytes) -> str:
    breakpoint()
    if str(size_bytes).isdigit():
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
    else:
        return size_bytes

def convert_to_bytes(max_size_string) -> int:
    if max_size_string.isdigit():
        return max_size_string
    else:
        desc = max_size_string[-2:]
        size = float(max_size_string[:-2])
        match desc.lower():
            case 'kb':
                max_size = size * 1024
            case 'mb':
                max_size = size * 1048576
            case 'gb':
                max_size = size * 1073741824
            case _:
                raise AttributeError('Unable to convert max upload size specifier')
        return int(math.ceil(max_size))
