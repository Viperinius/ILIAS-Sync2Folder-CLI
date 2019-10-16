# ILIAS-Sync2Folder-CLI
Command line version of ILIAS-Sync2Folder

## *Notice*
This is still in early development and not really functional yet.

## How to start the CLI after cloning
Open a virtual environment for python3
```sh
$ pip install virtualenv
$ virtualenv env
```
For Linux:
```sh
$ source env/bin/activate
```
For Windows:
```sh
$ env\Scripts\activate.bat
```
Both again (in your cloned directory):
```sh
$ pip install cliff
$ pip install -e .
```
You can use the programme then:
```sh
$ sync2folder <...>
```



## Used Python libraries
- [pyyaml](https://github.com/yaml/pyyaml) (MIT)
- [xmltodict](https://github.com/martinblech/xmltodict) (MIT)
- [zeep](https://github.com/mvantellingen/python-zeep) (MIT, other)
- [cliff](https://github.com/openstack/cliff) (Apache-2.0)
