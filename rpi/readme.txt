Download SD card image /tmp/2024-07-04-raspios-bookworm-armhf-lite.img.xz
unpack

unxz 2024-07-04-raspios-bookworm-armhf-lite.img.xz

check where is SD card

lsscsi

write image to SD card (be careful not to overwrite system disk)

dd if=2024-07-04-raspios-bookworm-armhf-lite.img of=/dev/sda

remove and insert SD card, mount vfat partition

mount /dev/sda1 /mt/usb/

Create a file named user userconf (or userconf.txt) containing the following:
pi:$6$c70VpvPsVNCG0YR5$l5vWWLsLko9Kj65gcQ8qvMkuOoRkEagI90qi3F/Y7rm8eNYZHW8CY6BOIKwMH7a3YYzZYL90zf304cAHLFaZE0
Place userconf (or userconf.txt) plus an empty file named ssh (or ssh.txt) in the BOOT (FAT32) partition of the SD card.
Insert the SD card in the Raspberry Pi and it should boot with access to user 'pi' (password : raspberry) via SSH.
@harphere

cd /mt/usb

echo "pi:$6$c70VpvPsVNCG0YR5$l5vWWLsLko9Kj65gcQ8qvMkuOoRkEagI90qi3F/Y7rm8eNYZHW8CY6BOIKwMH7a3YYzZYL90zf304cAHLFaZE0" > userconf.txt
touch ssh.txt

unmount and place SD card into raspberry

umount /dev/sdb1

power the raspberry, wait 1 minute to boot and login

ssh pi@raspberrypi.lan

copy files over the network

scp ../joystick.py 80-usbserial-startracker.rules startracker.service pi@raspberrypi.lan:~/

# for remote shooting from joystick blue btn:
# install chdk (1.6.1 known to work) and chdkptp raspbian (r964 known to work)
# chdkptp needs libusb 0.1
# apt install libusb-0.1-4
