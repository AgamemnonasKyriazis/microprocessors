import sys


def disp_progress_bar(low, high):
    remaining = high - low
    progress = int(100 - (100 * remaining) / high)
    sys.stdout.write('\r')
    sys.stdout.write(f"[{'='*progress}{' '*(100-progress)}] {progress}%")
    sys.stdout.flush()
    if progress == 99:
        disp_progress_bar(1, 1)
        sys.stdout.write('\n')
        sys.stdout.flush()