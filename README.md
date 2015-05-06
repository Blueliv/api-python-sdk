# Blueliv API Python SDK [![Build Status](https://secure.travis-ci.org/Blueliv/api-python-sdk.png?branch=master)](http://travis-ci.org/Blueliv/api-python-sdk)

Blueliv provides a simple Python-based API to access Blueliv's API and integrate it with other tools. This is the official API that is maintained by Blueliv ([community@blueliv.com](mailto:community@blueliv.com)).

The latest version can always be found [here](http://github.com/Blueliv/api-python-sdk).

## Minimum Requirements

* API key (get yours <a href="https://map.blueliv.com" target="_blank">here</a>)
* Python v2.7

## Installing
To use Bluelivs's Python API module, you need to place the package `api-python-sdk` in one of the directories specified by the environment variable `PYTHONPATH`. For more information on PYTHONPATH and using modules in Python, please read <a href="http://docs.python.org/tutorial/modules.html" target="_blank">this tutorial</a>.

### Installing with `pip`

#### Master 
If you wish to install the current `master`, use the following command (Note that `master` contains the latest revisions and is largely considered "stable" but it is not an official packaged release. If you want the latest packaged release, use the latest tag number):  
`pip install git+git://github.com/Blueliv/api-python-sdk`

#### Specific Versions 
To install a specific version of the package with `pip` (recommended), run the following command 
(This example installs the v1.0.0 tag. Replace the version tag with the one you want):  
`pip install git+git://github.com/Blueliv/api-python-sdk@v1.0.0`

#### requirements.txt
If you're using pip with `requirements.txt`, add the following line:  
`git+git://github.com/Blueliv/api-python-sdk`

## API Documentation
Detailed documentation about Blueliv's API is available on the <a href="https://github.com/Blueliv/api-python-sdk/wiki/Blueliv-REST-API-Documentation" target="_blank">Blueliv API Wiki</a>.

## Changelog

**v1.2.1 - 2015 May 06**

+ Change Travis CI script

**v1.2.0 - 2015 May 06**

+ Add HTTPS host verification
+ Improve logging

**v1.1.0 - 2015 Mar 26**

+ Add Bot IPs feed API

**v1.0.0 - 2015 Mar 05**

+ First version
