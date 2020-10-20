# GitHubMonitor
Commits monitoring of GitHub repositories with Python

## Data download

The goal was to dowload the list of contributors of a specific repository on GitHub, here the React repository owned by Facebook. I decided to simply use the API Rest with the /contributors/ endpoint. The challenge here was to get all the contributors who are spread wihin several pages. An iteration to traverse pages was necessary and was performed with a while loop checking if the current response, and so page, contained a link to the next page.

## Event monitoring

The monitoring consisted in inspecting contributors and triggering event if a contributor had less than 2 commits. The first step was a simple filter on the downloaded contributor list to retrieve the wanted contributor. Then, these contribrutors were added in a JSON file.

## Data visualization

I decided to draw 2 plots here. The first one is an histogram plot of the proportion of contributors in function of the number of contributions made. The second one share some common points as it also shows a repartiations of the data. Indeed, it plots the cumulated proportion of contributor in function of the number of contribution made.

## Global activity visualization

A pie plot was here interesting since it is able to compare the commitment of each contributors.



