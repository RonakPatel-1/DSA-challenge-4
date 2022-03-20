# DSA Challenge 4

import subprocess as s
import re

print("Welcome to File recovery DSA challenge - 4 by Ronak JitendraBhai Patel \n Please ensure you have some USB device mounted and you run this code on Ubuntu as pre-requiste with SleuthKit installed \n ")
t = s.Popen('lsblk -o NAME,MOUNTPOINT | grep -e "/media/"', stdout=s.PIPE, shell=True)
z = re.sub('[^A-Za-z0-9/ \n]+', '', t.stdout.read().decode('utf-8')).splitlines()

if not z:
    print("There is No partitions mounted. Please mount thumbdrive/USB <eom>")
    exit()
else:
    w = s.Popen('whoami', stdout=s.PIPE, shell=True).stdout.read().decode('ascii').strip()
    l, drives = list(), list()
    for i in z:
        l = i.split()
        drives.append(l)

    while(True):
        print('Below is the list of Partitions\n ')
        for i in range(1, len(drives) + 1):
            print(str(i) + '\t' + re.sub('/media/' + w + '/', '', drives[i-1][1]))

        c = int(input('Enter partition number which you want to examine\t: ' ))
        f = input('Please enter temp image name\t: ')
        s.Popen('umount /dev/' + drives[c-1][0], stdout=s.PIPE, shell=True)
        t1 = s.Popen('sudo dd if=/dev/' + drives[c-1][0] + ' of=' + f, stdin=s.PIPE, stdout=s.PIPE, shell=True)
        t1.communicate()
        files = list()
        c = s.Popen('fls ' + f + ' | grep -e "*"', stdout=s.PIPE, shell=True).stdout.read().decode('utf-8').splitlines()
        for i in c:
            l = i.split()
            l[2] = re.sub('[^0-9]+', '', l[2])
            files.append(l)
        
        if not files:
            print('There is no files availble which can be recovered in this partition!')
            exit()
        else:
            while(True):
                for i in range(1, len(files) + 1):
                    print(str(i) + '\t' + files[i-1][3])
                c = int(input('Please type the file to recover : '))
                print(s.Popen('istat ' + f + ' ' + files[c-1][2], stdout=s.PIPE, shell=True).stdout.read().decode('utf-8'))
                s.Popen('icat ' + f + ' ' + files[c-1][2] + ' > ' + files[c-1][3], stdout=s.PIPE, shell=True)
                c = input('Do you want to still check and continue recovering this partition? Enter Y:N')
                if c.lower() == 'n':
                    c = s.Popen('rm -f ' + f, stdout=s.PIPE, shell=True)
                    break

        c = input('Do you want to continue recovering from partitions apart from this? ')
        if c.lower() == 'n':
            exit()