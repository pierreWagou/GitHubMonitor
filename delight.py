import requests
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

class ApiError(Exception):
    """Exception to be raised when API does not return expected response"""
    pass

def get_page_data(previous_res):
    res = requests.get(previous_res.links['next']['url'])
    if res.status_code!=200:
        raise ApiError(f'Get /contributors/ {res.status_code}')
    return res

def get_contributors_list():
    url = 'https://api.github.com/repos/facebook/react/contributors?page=1'
    res = requests.get(url)
    contributor_list = res.json()
    while 'next' in res.links.keys():
        res = get_page_data(res)
        contributor_list.extend(res.json())
    return contributor_list

def monitor_event(contributor_list):
    event = [contributor for contributor in contributor_list if contributor['contributions']<2]
    with open('event.json', 'w+') as event_file:
        json.dump(event, event_file, sort_keys=True, indent=4)

def plot_cumulated_contributions(contributor_list):
    contributions_list = [contributor['contributions'] for contributor in contributor_list]
    counter = Counter(contributions_list)
    items = dict(sorted(counter.items()))
    keys = list(items.keys())
    values = list(items.values())
    cumsum = np.cumsum(values)
    plot = sns.lineplot(x=keys, y=cumsum)
    plot.set_xscale("log")
    plot.set_yscale("log")
    plot.set(xlabel="Contributions", ylabel="Proportion of contributors")
    plot.set_title("Cumulated proportion of contributors for each number of contributuon")
    plt.savefig("cumulated_contributions.png")
    plt.clf()

def plot_contributions(contributor_list):
    contributions_list = [contributor['contributions'] for contributor in contributor_list]
    plot = sns.histplot(contributions_list)
    plot.set_xscale("log")
    plot.set_yscale("log")
    plot.set(xlabel="Contributions", ylabel="Frequence of contributors")
    plot.set_title("Frequence of contributors in function of number of contributuon")
    plt.savefig("contributions.png")
    plt.clf()

def pie_plot(contributor_list):
    contributions_list = [contributor['contributions'] for contributor in contributor_list]
    contributor_login_list = [contributor['login'] for contributor in contributor_list]
    plot = plt.pie(x=contributions_list, labels=contributor_login_list, normalize = True)
    plt.savefig("contributors_pie.png")
    plt.clf()

contributor_list = get_contributors_list()
monitor_event(contributor_list)
plot_cumulated_contributions(contributor_list)
plot_contributions(contributor_list)
pie_plot(contributor_list)
