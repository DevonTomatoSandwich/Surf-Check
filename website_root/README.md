# website_root
This folder shows some contents that exists in the root folder for my website. My website uses react on the front end with flask to run the python code in the back end. 

# Differences to repl
Main difference is: A plot is returned (to be used in views.py) but no image is saved or shown. 
views.py will then use:
`flask.send_file(...` 
to send the image data which is recieved at the front end i.e. react/kook_check.js with a fetch method

There are also some differences with imports e.g. file structure and matplotlib.use('Agg').

# Why
I wanted to show this code so that more people could find out how to display a matplotlib chart in a react project.