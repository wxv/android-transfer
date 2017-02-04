#!/bin/env python3
# Trying to automate android backups but fed up with bash :(

import os
import subprocess
import sys

PHONE_BACKUP_DIR = "sdcard1/TWRP/BACKUPS/cb180349"  
PC_BACKUP_DIR = os.environ["HOME"] + "/TWRP-Backups"


def main():
    MTP_PATH = "/run/user/1000/gvfs"
    if not os.listdir(MTP_PATH):
        print("MTP path not found!")
        return

    mountpoint = os.listdir(MTP_PATH)[0]
    print("Using first mountpoint found:", mountpoint)

    
    phone_dir_full = MTP_PATH + '/' + mountpoint + '/' + PHONE_BACKUP_DIR
    if not os.listdir(phone_dir_full):
        print("No phone backups found in:", phone_dir_full)
        return

    phone_backup = os.listdir(phone_dir_full)[-1]
    print("Using last phone backup found:", phone_backup)

    phone_backup_full = phone_dir_full + '/' + phone_backup
    args = ["rsync", "-avP", phone_backup_full, PC_BACKUP_DIR]
    print("Starting subprocess with args", args)

    print()
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    
    # Get output of rsync --progress, otherwise not needed
    # From http://stackoverflow.com/a/803396/3163618
    while True:
        out = p.stdout.read(1)
        if not out and p.poll() != None:
            break
        if out:
            sys.stdout.write(out.decode("utf-8"))
            sys.stdout.flush()
            

if __name__ == "__main__": main()
