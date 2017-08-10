# SI-330-Homework-5-Six-degrees-of-Kevin-Bacon
Builds and visualizes a social network of movie actors from IMDB

Homework Instructions:

SI 330 Homework 5: Six degrees of Kevin Bacon
Due Date:  Fri. February 10, 11:59pm
Objectives:
Parsing HTML and JSON files
Learn to use Web APIs
Construction and visualization of networks
Continued practice manipulating delimited text files
Submission Instructions:
After completing this homework, you will turn in one file via Canvas ->  Assignments: a zip file named si330-hw5-YOUR_UNIQUE_NAME.zip that contains the following files: 
Your python script, named si330-hw5-YOUR_UNIQUE_NAME.py
Answers to textual questions, named si330-hw5-YOUR_UNIQUE_NAME.txt
All output files from the 6 steps below, including the final PNG image file of the graph.

This homework involves multiple steps: you will get credit for each step you complete successfully. You should complete the steps one by one and verify that you’ve completed each correctly before moving on to the next one.
In this assignment, you’ll build and visualize a social network of movie actors: the graph nodes will represent individual actors, and two actors will be connected by an edge in the graph if they co-starred at least one movie together from an IMDB top 100 movies list - with no edge between them otherwise.  To do this, you’ll apply your new knowledge of HTML parsing with BeautifulSoup and JSON processing, and get experience with a widely-used graph visualization package, GraphViz.

Step 0. Install GraphViz
First, you’ll need to install GraphViz  (http://www.graphviz.org) to get the gvedit application that draws the actor social network (parts of pydot also use graphviz).
Mac Version:  http://graphviz.org/Download_macos.php 
	(or preferably use brew install graphviz. You will need Homebrew for this.)
Windows Version:  http://graphviz.org/Download_windows.php
NOTE for Windows users: You will have to add the bin subdirectory of GraphViz to your PATH Environment variable. E.g. if you installed GraphViz in C:\Program Files (x86)\Graphviz2.38, add C:\Program Files (x86)\Graphviz2.38\bin to your PATH. See here for instructions on adding directories to your path in Windows.
You’ll also be using these packages for this homework, so make sure you have them installed:  
urllib, BeautifulSoup (bs4), re, json, pydot, time
Using the package itertools isn’t required but it makes one step in generating the graph easier and is a handy package to know about in general.

If you are using Anaconda’s Python3, conda install pydot might not work. In that case, run the following steps:
Run conda info
Go to the folder mentioned in “root environment”
cd bin
For windows, run: pip.exe install pydot or for unix like systems, run: ./pip install pydot

Else, if you are using your OS’s Python3 installation, use pip install pydot

How to test if you have these packages?
In PyCharm, go to Tools > Python Console, and type/paste this:
import urllib, bs4, re, json, pydot, time

If you get the exception, ImportError: No module named 'pydot' or equivalent, it means that particular package is missing.

Step 1. Fetch and save the IMDB top 100 movies page
Rename si330-homework-5-template.py to si330-hw5-YOUR_UNIQUE_NAME.py, then modify the step1_fetch_top_100_movies function so that it fetches the IMDB top 100 movies (by number of votes) page using this URL: http://www.imdb.com/search/title?at=0&sort=num_votes&count=100
and saves it in a HTML file named step1.html. The saved HTML file should look similar to step1_desired_output.html.  Note that a few movies have titles or actors with, e.g. accented characters. Make sure you use the utf-8 encoding to write out the HTML to use Unicode and preserve any non-English characters.

To avoid repeating this web request on re-runs, we check if step1.html already exists at the start of this function using os.path.exists("step1.html"). os.path.exists is part of the os python package, which is used to test if a file exists on your disk. It returns True if it exists, else it returns False. This technique of testing existence of a file, is used in all functions to avoid repeating a step which has already completed successfully and thus save time. 
 
Step 2. Parse the IMDB page to get movie titles
Modify the step2_extract_movie_info function so that it parses the HTML page above with BeautifulSoup, extracts movie information as described below, and saves the result in a tab-delimited file named step2.txt.  Your step2.txt file should have 3 columns and 100 rows. The 3 columns should be:
IMDB_ID
Rank
Title
The IMDB_ID is the part that sits between last two slashes in the movie URL in the table.
For example, if the URL is http://www.imdb.com/title/tt0111161/, the IMDB ID is tt0111161
Your tab-delimited step2.txt file should look like step2_desired_output_first50.txt. Here’s a sample of the first four lines:
 
tt0111161   1 	The Shawshank Redemption
tt0468569   2 	The Dark Knight
tt1375666   3 	Inception
tt0110912   4 	Pulp Fiction

Step 3. Use the OMDB Web API to fetch movie metadata
Modify the step3_get_metadata_using_omdb function so that it uses the Web service http://omdbapi.com/ to get movie metadata for each of the top 100 movies using the IMDB ID you collected in Step 2.  The API with sample requests is documented on the homepage. 
For example, this URL fetches JSON for the movie “The Social Network”, which has IMDB ID tt1285016: http://www.omdbapi.com/?i=tt1285016
 
You should see something like this JSON response:
{"Title":"The Social Network","Year":"2010","Rated":"PG-13","Released":"01 Oct 2010","Runtime":"120 min","Genre":"Biography, Drama","Director":"David Fincher","Writer":"Aaron Sorkin (screenplay), Ben Mezrich (book)","Actors":"Jesse Eisenberg, Rooney Mara, Bryan Barter, Dustin Fitzsimons","Plot":"Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook, but is later sued by two brothers who claimed he stole their idea, and the cofounder who was later squeezed out of the business.","Language":"English, French","Country":"USA","Awards":"Won 3 Oscars. Another 102 wins & 86 nominations.","Poster":"http://ia.media-imdb.com/images/M/MV5BMTM2ODk0NDAwMF5BMl5BanBnXkFtZTcwNTM1MDc2Mw@@._V1_SX300.jpg","Metascore":"95","imdbRating":"7.8","imdbVotes":"326,376","imdbID":"tt1285016","Type":"movie","Response":"True"}
 
NOTE: If you are having trouble getting access to the API due to 503 errors, we have mirrored the responses you need in order to complete the assignment. To use the mirror, change your API calls from something like this:
http://www.omdbapi.com/?i=tt0993846
To something like this:
http://www-personal.umich.edu/~mjskay/omdb_backup/tt0993846.json

IMPORTANT!  Make sure you call the time module function sleep(5) after each HTTP request call to urlopen to pause for 5 seconds.  We have added this call for you in the source file.  You MUST pause 5 seconds between EVERY HTTP request to omdbapi.com. If you don’t do this, and send requests omdbapi.com continuously in a loop with no delay, the server may reject your requests AND MAY EVEN SHUT DOWN.  (Yes, this has happened before.) 

Save your results in a text file named step3.txt that contains a JSON string for each movie on each line. The file should look like step3_desired_output_first50.txt.

Step 4. Save a JSON file with each actor's co-stars
Modify the step4_select_top4_actors function to open the file you saved in step 3. For every line in step3.txt, this function should load the JSON string into a variable and extract the movie title (as a string) and actors (as a python list), and place them into a dictionary representing that line. The dictionary representing each line is then placed into a list. The function should then save the resulting list-of-dictionaries in JSON format in a file named step4.json. This file will then contain a list of dictionaries with the keys:
Title (the value of which is a string)
Actors (the value of which is a list containing 4 actors from the actors list)

The file should look like step4_desired_output.json

Step 5. Plot the actor's "social network"
Modify the step5_create_dotviz_file to generate the DOT file containing the actor graph using the pydot module. After downloading and install GraphViz from http://www.graphviz.org/, you should install the pydot package in your usual way, e.g. pip install pydot or sudo pip install pydot. Read and try out the examples at http://pythonhaven.wordpress.com/tag/pydot/
 
Now load the file you saved in step 4 and generate a graph using the actor lists. Each actor will be a graph node, and if two actors are in the actors list (of the first four actors, that is) for the same movie, then there will be an edge between them in the graph. Save the resulting graph in a .dot file, which is a plain text file in the DOT language.  Note that we don’t want to save a PNG file: we want the DOT file instead. The pydot manual at http://code.google.com/p/pydot/downloads/list explains how to do this.
 
Save your .dot file to a file called actors_graph_output.dot. It should look like the file actors_graph_desired_output_first100.dot supplied in the homework ZIP file.
 
HINT:  Suppose A, B, C, D, E is the actors list for a movie. You’ll need to add edges for
every possible pairs of actors in this list, e.g. (A, B)  (A, C) etc. This is where the optional itertools module will come in useful, if you choose to use it.  The combinations method will generate every possible pair of elements, given a list.
 
Step 6. Save an image of the network 
Open the saved actors_graph_output.dot file you created in step 5 using the gvedit application that comes with GraphViz. Using the Graph/Settings dialog, save the graph visualization in a PNG image file named actors_graph.png, which should look like actors_graph_desired_output.png provided in the homework ZIP file.  

MacOS users can use the command dot -Tpng actors_graph_output.dot > actors_graph.png
 

