# Catapult

A simple multi server deployer

Usage:

`./catapult.py <source_dir> <yml_data>`

catapult will copy all files inside source_dir to server directory defined in yaml path

Sample Yaml data format:

```
clientname1:
    host: example.com
    user: ftp_user_name
    pass: ftp_password
    path: public_html
clientname2:
    host: example1.com
    user: ftp_user_name
    pass: ftp_password
    path: httpdoc
clientname3:
    host: example1.com
    user: ftp_user_name
    pass: ftp_password
    path: www
```
to update only one server you can use --only

`./catapult.py <source_dir> <yml_data> --only=clientname3`