import datetime
import glob
import multiprocessing
import os

from PIL import Image, ImageDraw

from task import DOWNLOAD_DIR

IMG_DIR = './flags_plus'
COLOUR = 'black'
BOARDER_LINE = 1


def redraw_image(img_sourse, img_out):
    image = Image.open(img_sourse)
    draw = ImageDraw.Draw(image)
    draw.rectangle(xy=((0,0),(image.size[0] - 1, image.size[1] - 1)), width=BOARDER_LINE, outline=COLOUR)
    image.save(img_out)

    return os.path.getsize(img_out)


def queue_forming(set_flags):
    tuple_queue = []
    for flag in set_flags:
        output_flag = os.path.join(IMG_DIR, flag[8:])
        tuple_queue.append((flag[8:-4], os.path.getsize(flag), redraw_image(flag, output_flag)))

    return tuple_queue


def simple_redrawing(set_flags):
    return queue_forming(set_flags)


def multi_threading_redrawing(set_flags):
    process_count = multiprocessing.cpu_count()
    quantity_of_items = len(set_flags) // process_count

    processes = []

    for i in range(process_count):
        set_for_one_process = set_flags[i * quantity_of_items :(i + 1) * quantity_of_items  - 1]
        process = multiprocessing.Process(
            target=queue_forming,
            args=set_for_one_process
        )
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
    flags = glob.glob(os.path.join(DOWNLOAD_DIR, '*.png'))

    multi_threading_redrawing_start = datetime.datetime.now()
    multi_threading_redrawing(flags)
    multi_threading_redrawing_stop = datetime.datetime.now() - multi_threading_redrawing_start

    simple_redrawing_start = datetime.datetime.now()
    data = simple_redrawing(flags)
    for item in data:
        print(item)
    print(multi_threading_redrawing_stop, datetime.datetime.now() - simple_redrawing_start)
