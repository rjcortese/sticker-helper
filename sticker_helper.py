from PIL import Image, ImageOps
from pathlib import Path
from zipfile import ZipFile

print("woof")

def unzip(zipfile, original):
    """ Unzip the `zipfile` full of images into the dir `original`.
    """
    with ZipFile(zipfile) as zf:
        zf.extractall(original)

def read_transform_write(imgin, outdir):
    """ Read the image file `imgin`.
        Transform it by calling the `transform` function.
        Write the result to `imgout`.
    """
    print(f"{imgin = }")
    outfile = outdir / imgin.with_suffix(".webp").name
    print(f"{outfile = }")
    try:
        with Image.open(imgin) as img:
            print(f"{img.format = }, {img.size = }, {img.mode = }")
            out = ImageOps.pad(img, (512, 512), color="#ffffff").convert("RGBA")
            data = out.getdata()
            updated_data = []
            for d in data:
                if d[0] == 255 and d[1] == 255 and d[2] == 255:
                    updated_data.append((255, 255, 255, 0))
                else:
                    updated_data.append(d)
            out.putdata(updated_data)
            out.save(outfile)
    except Exception as e:
        print(f"caught execption trying to process {imgin}: {e}")
        


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("zipfile")
    
    args = parser.parse_args()
    args.zipfile = Path(args.zipfile)
    args.basedir = args.zipfile.parent
    args.original = args.basedir / "original"
    # output dir for processed webp images we create
    args.webp = args.basedir / "webp"
    print(f"{args = }")

    args.webp.mkdir(exist_ok=True)

    unzip(args.zipfile, args.original)

    for path in args.original.iterdir():
        read_transform_write(path, args.webp)
