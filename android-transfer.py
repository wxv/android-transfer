#!/bin/env python3
# Trying to automate android backups but fed up with bash :(

# TODO: Nicer mode selection?

import os
import subprocess
import sys

SD_DIR = "sdcard1"
PHONE_BACKUP_DIR = "sdcard1/TWRP/BACKUPS/cb180349"
PC_BACKUP_DIR = os.environ["HOME"] + "/TWRP-Backups"
MTP_PATH = "/run/user/1000/gvfs"
DATA_MEDIA_PATH = "Internal shared storage"


def main(backup_mode=0, append=False):
    if not os.listdir(MTP_PATH):
        print("MTP path not found!")
        return

    mountpoint = os.listdir(MTP_PATH)[0]
    print("Using first mountpoint found:", mountpoint)

    phone_path = os.path.join(MTP_PATH, mountpoint)

    if backup_mode == 0:
        # Transfer last backup found in PHONE_BACKUP_DIR
        phone_dir_full = os.path.join(phone_path, PHONE_BACKUP_DIR)
        if not os.listdir(phone_dir_full):
            print("No phone backups found in:", phone_dir_full)
            return

        phone_backup = os.listdir(phone_dir_full)[-1]
        print("Using last phone backup found:", phone_backup)

        src_path_final = os.path.join(phone_dir_full, phone_backup)

    elif backup_mode == 1:
        # Transfer contents of SD card
        src_path_final = os.path.join(phone_path, SD_DIR)

    elif backup_mode == 2:
        # Transfer everything in data/media (or "Internal shared storage")
        src_path_final = os.path.join(MTP_PATH, mountpoint, DATA_MEDIA_PATH)

    else:
        print("Unrecognized mode")
        return


    flags = ["-av", "--progress"]
    if append: flags.append("--append-verify")
    args = ["rsync"] + flags + [src_path_final, PC_BACKUP_DIR]

    print("Starting subprocess with args", args)
    print()

    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    
    # Get output of rsync --progress, otherwise not needed
    while True:
        out = p.stdout.read(1)
        if not out and p.poll() != None:
            break
        if out:
            sys.stdout.write(out.decode("utf-8"))
            sys.stdout.flush()
            

if __name__ == "__main__":
    main(backup_mode=0, append=True)
