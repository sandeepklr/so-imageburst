import exifread
import sys
import glob
import os.path
import matplotlib.pyplot as plt
import dateutil.parser as parser
import matplotlib.cm as cm
import numpy as np


if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)

    if argc < 2:
        sys.exit("Usage: {0} folder1 [folder2 ...]".format(argv[0]))

    folders = argv[1:]

    times = []

    i = 1
    inter = []
    t2 = None
    for folder in folders:
        t1 = None
        img_files = glob.glob(os.path.join(folder, "*.JPG"))
        print "folder: {0}".format(folder)

        intra = 0.
        max_intra = -sys.maxsize
        min_intra = sys.maxsize

        j = 0
        for img_file in img_files:
            print "\t file: {0}".format(img_file)
            with open(img_file, "rb") as f:
                tags = exifread.process_file(f)
                print "\t\t{0}".format(tags["EXIF DateTimeOriginal"])

                t = parser.parse(str(tags["EXIF DateTimeOriginal"]))

                times.append((i, t))

                # Statistics:
                if t1 is None:
                    t1 = t
                    if t2 is not None:
                        inter.append(abs((t2 - t1).total_seconds()))
                else:
                    t2 = t
                    diff = abs((t2 - t1).total_seconds())
                    intra += diff

                    if diff < min_intra:
                        min_intra = diff
                    if diff > max_intra:
                        max_intra = diff

                    t1 = t2

            j += 1

        print "Total image files in folder: {0}".format(j)
        print "Total intra-cluster time: {0}".format(intra)
        print "Average intra-cluster time: {0}".format(intra/j)
        print "Max: {0}, Min: {1}".format(max_intra, min_intra)
        print ""

        i += 1

    print "Inter-cluster times: {0}".format(inter)

    xs = [time[1] for time in times]
    ys = [time[0] for time in times]

    colors = cm.rainbow(np.linspace(0, 1, i))

    for x, y in zip(xs, ys):
        plt.scatter(x, 1, color=colors[y])

    plt.show()
