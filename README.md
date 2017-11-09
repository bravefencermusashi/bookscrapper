# bookscrapper
Automatic download of it ebooks on allitebooks

## usage

<pre>
usage: scrapbook [-h] [-q] {get,create-conf} ...

positional arguments:
  {get,create-conf}  script main command
    get              retrieve books
    create-conf      create the default config file and give its location

usage: scrapbook get [-h] keyword [keyword ...]

positional arguments:
  keyword     search keywords separated by spaces

usage: scrapbook create-conf [-h]
</pre>

## installation

Change directory to be at the root level of the project (at the setup.py level) and run:
<pre>
pip install .
</pre>
The program will then be available at the system level.

## configuration

There is an hardcoded default configuration. But you can override it by providing a configuration file :
<pre>
~/.bookscrapper
</pre>
You can create that file manually and override what you want. But it has to comply to the expected format (JSON).
The recommended way is use the dedicated scrapbook command :
<pre>
scrapbook create-conf
</pre>
This will automatically create the configuration file with the default values. You can then change them.<br/>
Here are the properties you can modify :
<ul>
    <li>library_path : root directory of the place where books will be downloaded
    <li>dl_link_dump_path : a directory where download links for different searches are stored
    <li>managed_extensions : will look for files with those extensions in the library when looking for already
    downloaded books
    <li>dummy_books_extension : when a dummy book is created, it will have this extension
</ul>

## requirements

This program is coded in Python 3
