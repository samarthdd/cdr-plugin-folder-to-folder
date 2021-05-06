import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    version                       = "0.1.0"               , # change this on every release
    name                          = "cdr-plugin-folder-to-folder"  ,
    author                        = "Dinis Cruz",
    author_email                  = "dcruz@glasswallsolutions.com",
    description                   = "Glasswall CDR Platform Plugin - Folder to Folder",
    long_description              = long_description,
    long_description_content_type = " text/markdown",
    url                           = "https://github.com/filetrust/cdr-plugin-folder-to-folder",
    packages                      = setuptools.find_packages(),
    classifiers                   = [ "Programming Language :: Python :: 3"   ,
                                      "License :: OSI Approved :: MIT License",
                                      "Operating System :: OS Independent"   ])
