# bookscrapper
Automatic download of it ebooks on allitebooks.com

## configuration
Configuration is in the conf.py file. Edit the scrapper dictionary to change the configuration.
<ul>
    <li>library_path : root directory of the place where books will be downloaded
    <li>dl_link_dump_path : a directory where download links for different searches are stored
    <li>managed_extensions : will look for files with this extension in the library when looking for already
    downloaded books
    <li>dummy_books_extension : when a dummy book is created, it will have this extension
</ul>

## dependencies
<ul>
    <li>requests
    <li>beautifulsoup 4
    <li>lxml (for beautifulsoup)
</ul>

