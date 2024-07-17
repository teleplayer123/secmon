import cv2
import os

IMGSHAPE = lambda fn: cv2.imread(fn).shape
IMGEXTRACT = lambda fn: cv2.imread(fn)

CVT_TYPES = {
    "gray2rgb": cv2.COLOR_GRAY2RGB,
    "gray2rgba": cv2.COLOR_GRAY2RGBA,
    "gray2bgr": cv2.COLOR_GRAY2BGR,
    "bgr2rgb": cv2.COLOR_BGR2RGB,
    "bgr2rgba": cv2.COLOR_BGR2RGBA,
    "bgr2gray": cv2.COLOR_BGR2GRAY,
    "rgb2gray": cv2.COLOR_RGB2GRAY,
    "rgb2bgr": cv2.COLOR_RGB2BGR,
    "rgb2rgba": cv2.COLOR_RGB2RGBA,
    "rgba2rgb": cv2.COLOR_RGBA2RGB,
    "rgba2bgr": cv2.COLOR_RGBA2BGR,
    "rgba2gray": cv2.COLOR_RGBA2GRAY,
}

THRESHOLD_TYPES = {
    "binary": cv2.THRESH_BINARY,
    "binary_inv": cv2.THRESH_BINARY_INV,
    "trunc": cv2.THRESH_TRUNC,
    "tozero": cv2.THRESH_TOZERO,
    "tozero_inv": cv2.THRESH_TOZERO_INV,
}

def convert_pixel_type(filename: str, outfilename: str, src_type: str="bgr", dest_type: str="rgba") -> str:
    """
    @param str filename: path to image to convert
    @param str outfilename: name of file to save result in results folder
    @param str src_type: image pixel type before converting
        @args: 'gray', 'bgr', 'rgb', 'rgba'
    @param str dest_type: pixel type to convert image
        @args: 'gray', 'bgr', 'rgb', 'rgba'
    @returns str outfile: path where converted image was saved
    """
    outdir = os.path.join(os.getcwd(), "results")
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    outfile = os.path.join(outdir, outfilename)
    cvt_type_str = "{}2{}".format(src_type.lower(), dest_type.lower())
    cvt_type = CVT_TYPES[cvt_type_str]
    im = cv2.imread(filename)
    cvt_im = cv2.cvtColor(im, cvt_type)
    cv2.imwrite(outfile, cvt_im)
    return outfile


def threshold_image_gs(filename: str, threshold_type: str, threshold: int=127, threshold_max: int=255):
    try:
        thresh_type = THRESHOLD_TYPES[threshold_type.lower()]
    except KeyError:
        print("Inavlid Threshold Type, Available Types: {}".format(str(THRESHOLD_TYPES.keys())))
        return
    im = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    ret, thresh_img = cv2.threshold(im, threshold, threshold_max, thresh_type)
    outdir = os.path.join(os.getcwd(), "Results")
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    file_ext = filename.split(".")[-1]
    outfile = os.path.join(outdir, f"{filename.split('.')[0]}_{threshold_type}.{file_ext}")
    cv2.imwrite(outfile, thresh_img)
    return outfile