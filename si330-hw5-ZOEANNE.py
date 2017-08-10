#!/usr/bin/python

from urllib.request import urlopen
from bs4 import BeautifulSoup
import os, re, json
import pydot
import itertools
import csv
import time


def main():
    print("Step 1")
    step1_fetch_top_100_movies()
    print("Step 2")
    step2_extract_movie_info()
    print("Step 3")
    step3_get_metadata_using_omdb()
    print("Step 4")
    step4_select_top4_actors()
    print("Step 5")
    step5_create_graphviz_dot_file()


def step1_fetch_top_100_movies():
    '''
        Fetch the IMDB top 100 movies page (sorted by number of votes)
        and save the html content in step1.html
    '''
    if os.path.exists('step1.html'):
        # Step1: top 100 movies already fetched. Don't repeat!
        return

    # 1. Get response
    with urlopen('http://www.imdb.com/search/title?at=0&sort=num_votes&count=100') as response:
        # print(response.code)

    # 2. Read response html into html variable
        html = response.read().decode("utf-8")


    # 3. Write response html into step1.html
    with open('step1.html', 'w', encoding="utf-8") as outfile:
        outfile.write(html)


def step2_extract_movie_info():
    '''
        Parse step1.html using BeautifulSoup.

        Observe its tree structure.
        (To do this, you can open step1.html in your browser,
        right click on the page and click on "Inspect Element").

        You need to extract IMDB_ID, Rank, Title for each movie.
        Think about where this information exists in the html.

        Store result in step2.txt
    '''
    if os.path.exists('step2.txt'):
        # If step 2 is already done, don't repeat!
        return

    # 1. Read step1.html
    # Read in binary mode (... 'rb') instead of (... 'r', encoding='utf-8')
    # because BeautifulSoup will decode the file from utf-8 itself
    with open('step1.html', 'rb') as infile:
        html = infile.read()

    # 2. Parse using BeautifulSoup
    # If you get a warning, use: BeautifulSoup(YOUR_HTML_VARIABLE, "html.parser")
    soup = BeautifulSoup(html, "html.parser")

    # 3. Find all movie rows
    movie_rows = soup.find_all("div", class_="lister-item mode-advanced")

    # 4. Loop through each movie row,
    #    use beautiful soup to
    #    extract IMDB_ID, Rank, Title
    movie_list = []
    for row in movie_rows:
        movie = {}
        # set IMDB_ID, Title and Rank in movie dictionary
        string = row.h3.a.get("href")
        match = re.findall("t{2}\d{7}", string)
        movie["IMDB_ID"] = ''.join(match)
        movie["Title"] = row.h3.a.text
        movie["Rank"] = row.h3.span.text.replace(".","")

        movie_list.append(movie)

    # 5. Store this list of movie data as a tab-delimited file called step2.txt
    with open('step2.txt', 'w', newline='', encoding="utf-8") as outfile:
        data_writer = csv.DictWriter(outfile,
                                     fieldnames=['IMDB_ID', 'Rank', 'Title'],
                                     extrasaction='ignore',
                                     delimiter='\t', quotechar='"')
        data_writer.writeheader()
        data_writer.writerows(movie_list)


def step3_get_metadata_using_omdb():
    '''
        Use OMDB API to get each movie's metadata as JSON.
        Collect each movie's JSON in a list.
        Store each JSON as a row in step3.txt
    '''
    if os.path.exists('step3.txt'):
        # don't repeat this step if already done
        return

    # 1. Read step2.txt for IMDB_ID, which will be used in OMDB request
    with open('step2.txt', 'r', encoding="utf-8") as infile:
        movie_reader = csv.DictReader(infile, delimiter='\t', quotechar='"')

        # 2. For each movie, use OMDB API to get JSON metadata and store it in 'out' list
        out = []
        count = 0
        total = 100
        for movie in movie_reader:
            base_url = "http://www.omdbapi.com/?i="
            parameter = movie["IMDB_ID"]
            with urlopen(base_url + parameter) as response:
                json = response.read().decode("utf-8")
                out.append(json)

            count += 1
            print('{0:3}/{1}'.format(count, total))

            # ----------------------------------------------------------------
            # IMPORTANT: wait 5 seconds after each request using time.sleep(5)
            # ----------------------------------------------------------------
            time.sleep(5)

        print('')

    # 3. Store each JSON in that list as a line in step3.txt
    with open('step3.txt', 'w', encoding='utf-8') as outfile:
        json_strings = '\n'.join(out)
        outfile.write(json_strings)


def step4_select_top4_actors():
    '''
        Use JSONs from step3.txt and get top 4 actors for each movie
        Store this information in a tab-delimited file with columns Title and Actors,
            where Actors is a JSON list
    '''
    if os.path.exists('step4.json'):
        return

    # 1. Read step3.txt
    with open('step3.txt', 'r', encoding='utf-8') as infile:

        # 2. Loop through each of its row, load the JSON
        #    and extract just the Title and Actors.
        #    The JSON contains only have first *4 actors* from the actors list (separated by ', ').
        data = []
        for line in infile:
            movie = json.loads(line)
            title = movie["Title"]
            actors = movie["Actors"].split(", ")

            data.append({
                'Title': title,
                'Actors': actors
            })

    # 3. Write a json file containing a list of dictionaries with keys Title and Actors
    with open('step4.json', 'w', newline='', encoding="utf-8") as outfile:
        outfile.write(json.dumps(data))


def step5_create_graphviz_dot_file():
    '''
        Use Actors from step4.txt to create a social network graph.
        We will store this graph as a 'dot' file: actors_graph_output.dot
    '''
    # 1. Read step4.txt
    with open('step4.json', 'r', encoding="utf-8") as infile:
        movie_data = json.loads(infile.read())

    # 2. Initialize the graph using pydot
    graph = pydot.Dot(graph_type='graph', charset='utf8')

    # 3. For each movie, create pairs of actors (use itertools' combination method),
    #    where each pair will be used to make an edge in the graph

    count = 0
    for movie in movie_data:

        # use itertools' combinations method to create pairs
        actors = movie["Actors"]
        actor_pairs = itertools.combinations(actors, 2)

        for p in actor_pairs:
            # Then create an edge object and add that edge object to the graph
            edge = pydot.Edge(p[0], p[1])
            graph.add_edge(edge)
            count += 1

    print('Added {0} edges to the graph'.format(count))

    # 4. Write the dot file
    print('Writing graph file ...')
    graph.write('actors_graph_output.dot')


if __name__ == '__main__':
    main()
