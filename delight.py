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

contributor_list = [
  {"login": "zpao",
    'id': 8445, 'node_id': 'MDQ6VXNlcjg0NDU=', 'avatar_url': 'https://avatars1.githubusercontent.com/u/8445?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/zpao', 'html_url': 'https://github.com/zpao', 'followers_url': 'https://api.github.com/users/zpao/followers', 'following_url': 'https://api.github.com/users/zpao/following{/other_user}', 'gists_url': 'https://api.github.com/users/zpao/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/zpao/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/zpao/subscriptions', 'organizations_url': 'https://api.github.com/users/zpao/orgs', 'repos_url': 'https://api.github.com/users/zpao/repos', 'events_url': 'https://api.github.com/users/zpao/events{/privacy}', 'received_events_url': 'https://api.github.com/users/zpao/received_events', 'type': 'User', 'site_admin': False, 'contributions': 1777}, {'login': 'gaearon', 'id': 810438, 'node_id': 'MDQ6VXNlcjgxMDQzOA==', 'avatar_url': 'https://avatars0.githubusercontent.com/u/810438?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/gaearon', 'html_url': 'https://github.com/gaearon', 'followers_url': 'https://api.github.com/users/gaearon/followers', 'following_url': 'https://api.github.com/users/gaearon/following{/other_user}', 'gists_url': 'https://api.github.com/users/gaearon/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/gaearon/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/gaearon/subscriptions', 'organizations_url': 'https://api.github.com/users/gaearon/orgs', 'repos_url': 'https://api.github.com/users/gaearon/repos', 'events_url': 'https://api.github.com/users/gaearon/events{/privacy}', 'received_events_url': 'https://api.github.com/users/gaearon/received_events', 'type': 'User', 'site_admin': False, 'contributions': 1547}, {'login': 'bvaughn', 'id': 29597, 'node_id': 'MDQ6VXNlcjI5NTk3', 'avatar_url': 'https://avatars0.githubusercontent.com/u/29597?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/bvaughn', 'html_url': 'https://github.com/bvaughn', 'followers_url': 'https://api.github.com/users/bvaughn/followers', 'following_url': 'https://api.github.com/users/bvaughn/following{/other_user}', 'gists_url': 'https://api.github.com/users/bvaughn/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/bvaughn/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/bvaughn/subscriptions', 'organizations_url': 'https://api.github.com/users/bvaughn/orgs', 'repos_url': 'https://api.github.com/users/bvaughn/repos', 'events_url': 'https://api.github.com/users/bvaughn/events{/privacy}', 'received_events_url': 'https://api.github.com/users/bvaughn/received_events', 'type': 'User', 'site_admin': False, 'contributions': 1435}, {'login': 'sophiebits', 'id': 6820, 'node_id': 'MDQ6VXNlcjY4MjA=', 'avatar_url': 'https://avatars2.githubusercontent.com/u/6820?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/sophiebits', 'html_url': 'https://github.com/sophiebits', 'followers_url': 'https://api.github.com/users/sophiebits/followers', 'following_url': 'https://api.github.com/users/sophiebits/following{/other_user}', 'gists_url': 'https://api.github.com/users/sophiebits/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/sophiebits/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/sophiebits/subscriptions', 'organizations_url': 'https://api.github.com/users/sophiebits/orgs', 'repos_url': 'https://api.github.com/users/sophiebits/repos', 'events_url': 'https://api.github.com/users/sophiebits/events{/privacy}', 'received_events_url': 'https://api.github.com/users/sophiebits/received_events', 'type': 'User', 'site_admin': False, 'contributions': 1268}, {'login': 'sebmarkbage', 'id': 63648, 'node_id': 'MDQ6VXNlcjYzNjQ4', 'avatar_url': 'https://avatars2.githubusercontent.com/u/63648?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/sebmarkbage', 'html_url': 'https://github.com/sebmarkbage', 'followers_url': 'https://api.github.com/users/sebmarkbage/followers', 'following_url': 'https://api.github.com/users/sebmarkbage/following{/other_user}', 'gists_url': 'https://api.github.com/users/sebmarkbage/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/sebmarkbage/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/sebmarkbage/subscriptions', 'organizations_url': 'https://api.github.com/users/sebmarkbage/orgs', 'repos_url': 'https://api.github.com/users/sebmarkbage/repos', 'events_url': 'https://api.github.com/users/sebmarkbage/events{/privacy}', 'received_events_url': 'https://api.github.com/users/sebmarkbage/received_events', 'type': 'User', 'site_admin': False, 'contributions': 846}, {'login': 'acdlite', 'id': 3624098, 'node_id': 'MDQ6VXNlcjM2MjQwOTg=', 'avatar_url': 'https://avatars0.githubusercontent.com/u/3624098?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/acdlite', 'html_url': 'https://github.com/acdlite', 'followers_url': 'https://api.github.com/users/acdlite/followers', 'following_url': 'https://api.github.com/users/acdlite/following{/other_user}', 'gists_url': 'https://api.github.com/users/acdlite/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/acdlite/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/acdlite/subscriptions', 'organizations_url': 'https://api.github.com/users/acdlite/orgs', 'repos_url': 'https://api.github.com/users/acdlite/repos', 'events_url': 'https://api.github.com/users/acdlite/events{/privacy}', 'received_events_url': 'https://api.github.com/users/acdlite/received_events', 'type': 'User', 'site_admin': False, 'contributions': 797}, {'login': 'jimfb', 'id': 9595985, 'node_id': 'MDQ6VXNlcjk1OTU5ODU=', 'avatar_url': 'https://avatars3.githubusercontent.com/u/9595985?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/jimfb', 'html_url': 'https://github.com/jimfb', 'followers_url': 'https://api.github.com/users/jimfb/followers', 'following_url': 'https://api.github.com/users/jimfb/following{/other_user}', 'gists_url': 'https://api.github.com/users/jimfb/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/jimfb/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/jimfb/subscriptions', 'organizations_url': 'https://api.github.com/users/jimfb/orgs', 'repos_url': 'https://api.github.com/users/jimfb/repos', 'events_url': 'https://api.github.com/users/jimfb/events{/privacy}', 'received_events_url': 'https://api.github.com/users/jimfb/received_events', 'type': 'User', 'site_admin': False, 'contributions': 456}, {'login': 'trueadm', 'id': 1519870, 'node_id': 'MDQ6VXNlcjE1MTk4NzA=', 'avatar_url': 'https://avatars0.githubusercontent.com/u/1519870?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/trueadm', 'html_url': 'https://github.com/trueadm', 'followers_url': 'https://api.github.com/users/trueadm/followers', 'following_url': 'https://api.github.com/users/trueadm/following{/other_user}', 'gists_url': 'https://api.github.com/users/trueadm/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/trueadm/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/trueadm/subscriptions', 'organizations_url': 'https://api.github.com/users/trueadm/orgs', 'repos_url': 'https://api.github.com/users/trueadm/repos', 'events_url': 'https://api.github.com/users/trueadm/events{/privacy}', 'received_events_url': 'https://api.github.com/users/trueadm/received_events', 'type': 'User', 'site_admin': False, 'contributions': 436}, {'login': 'petehunt', 'id': 239742, 'node_id': 'MDQ6VXNlcjIzOTc0Mg==', 'avatar_url': 'https://avatars0.githubusercontent.com/u/239742?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/petehunt', 'html_url': 'https://github.com/petehunt', 'followers_url': 'https://api.github.com/users/petehunt/followers', 'following_url': 'https://api.github.com/users/petehunt/following{/other_user}', 'gists_url': 'https://api.github.com/users/petehunt/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/petehunt/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/petehunt/subscriptions', 'organizations_url': 'https://api.github.com/users/petehunt/orgs', 'repos_url': 'https://api.github.com/users/petehunt/repos', 'events_url': 'https://api.github.com/users/petehunt/events{/privacy}', 'received_events_url': 'https://api.github.com/users/petehunt/received_events', 'type': 'User', 'site_admin': False, 'contributions': 332}, {'login': 'chenglou', 'id': 1909539, 'node_id': 'MDQ6VXNlcjE5MDk1Mzk=', 'avatar_url': 'https://avatars2.githubusercontent.com/u/1909539?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/chenglou', 'html_url': 'https://github.com/chenglou', 'followers_url': 'https://api.github.com/users/chenglou/followers', 'following_url': 'https://api.github.com/users/chenglou/following{/other_user}', 'gists_url': 'https://api.github.com/users/chenglou/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/chenglou/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/chenglou/subscriptions', 'organizations_url': 'https://api.github.com/users/chenglou/orgs', 'repos_url': 'https://api.github.com/users/chenglou/repos', 'events_url': 'https://api.github.com/users/chenglou/events{/privacy}', 'received_events_url': 'https://api.github.com/users/chenglou/received_events', 'type': 'User', 'site_admin': False, 'contributions': 222}, {'login': 'vjeux', 'id': 197597, 'node_id': 'MDQ6VXNlcjE5NzU5Nw==', 'avatar_url': 'https://avatars0.githubusercontent.com/u/197597?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/vjeux', 'html_url': 'https://github.com/vjeux', 'followers_url': 'https://api.github.com/users/vjeux/followers', 'following_url': 'https://api.github.com/users/vjeux/following{/other_user}', 'gists_url': 'https://api.github.com/users/vjeux/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/vjeux/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/vjeux/subscriptions', 'organizations_url': 'https://api.github.com/users/vjeux/orgs', 'repos_url': 'https://api.github.com/users/vjeux/repos', 'events_url': 'https://api.github.com/users/vjeux/events{/privacy}', 'received_events_url': 'https://api.github.com/users/vjeux/received_events', 'type': 'User', 'site_admin': False, 'contributions': 207}, {'login': 'benjamn', 'id': 5750, 'node_id': 'MDQ6VXNlcjU3NTA=', 'avatar_url': 'https://avatars0.githubusercontent.com/u/5750?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/benjamn', 'html_url': 'https://github.com/benjamn', 'followers_url': 'https://api.github.com/users/benjamn/followers', 'following_url': 'https://api.github.com/users/benjamn/following{/other_user}', 'gists_url': 'https://api.github.com/users/benjamn/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/benjamn/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/benjamn/subscriptions', 'organizations_url': 'https://api.github.com/users/benjamn/orgs', 'repos_url': 'https://api.github.com/users/benjamn/repos', 'events_url': 'https://api.github.com/users/benjamn/events{/privacy}', 'received_events_url': 'https://api.github.com/users/benjamn/received_events', 'type': 'User', 'site_admin': False, 'contributions': 140}, {'login': 'yungsters', 'id': 55161, 'node_id': 'MDQ6VXNlcjU1MTYx', 'avatar_url': 'https://avatars0.githubusercontent.com/u/55161?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/yungsters', 'html_url': 'https://github.com/yungsters', 'followers_url': 'https://api.github.com/users/yungsters/followers', 'following_url': 'https://api.github.com/users/yungsters/following{/other_user}', 'gists_url': 'https://api.github.com/users/yungsters/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/yungsters/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/yungsters/subscriptions', 'organizations_url': 'https://api.github.com/users/yungsters/orgs', 'repos_url': 'https://api.github.com/users/yungsters/repos', 'events_url': 'https://api.github.com/users/yungsters/events{/privacy}', 'received_events_url': 'https://api.github.com/users/yungsters/received_events', 'type': 'User', 'site_admin': False, 'contributions': 120}, {'login': 'subtleGradient', 'id': 4117, 'node_id': 'MDQ6VXNlcjQxMTc=', 'avatar_url': 'https://avatars2.githubusercontent.com/u/4117?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/subtleGradient', 'html_url': 'https://github.com/subtleGradient', 'followers_url': 'https://api.github.com/users/subtleGradient/followers', 'following_url': 'https://api.github.com/users/subtleGradient/following{/other_user}', 'gists_url': 'https://api.github.com/users/subtleGradient/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/subtleGradient/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/subtleGradient/subscriptions', 'organizations_url': 'https://api.github.com/users/subtleGradient/orgs', 'repos_url': 'https://api.github.com/users/subtleGradient/repos', 'events_url': 'https://api.github.com/users/subtleGradient/events{/privacy}', 'received_events_url': 'https://api.github.com/users/subtleGradient/received_events', 'type': 'User', 'site_admin': False, 'contributions': 115}, {'login': 'nhunzaker', 'id': 590904, 'node_id': 'MDQ6VXNlcjU5MDkwNA==', 'avatar_url': 'https://avatars3.githubusercontent.com/u/590904?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/nhunzaker', 'html_url': 'https://github.com/nhunzaker', 'followers_url': 'https://api.github.com/users/nhunzaker/followers', 'following_url': 'https://api.github.com/users/nhunzaker/following{/other_user}', 'gists_url': 'https://api.github.com/users/nhunzaker/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/nhunzaker/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/nhunzaker/subscriptions', 'organizations_url': 'https://api.github.com/users/nhunzaker/orgs', 'repos_url': 'https://api.github.com/users/nhunzaker/repos', 'events_url': 'https://api.github.com/users/nhunzaker/events{/privacy}', 'received_events_url': 'https://api.github.com/users/nhunzaker/received_events', 'type': 'User', 'site_admin': False, 'contributions': 94}, {'login': 'necolas', 'id': 239676, 'node_id': 'MDQ6VXNlcjIzOTY3Ng==', 'avatar_url': 'https://avatars2.githubusercontent.com/u/239676?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/necolas', 'html_url': 'https://github.com/necolas', 'followers_url': 'https://api.github.com/users/necolas/followers', 'following_url': 'https://api.github.com/users/necolas/following{/other_user}', 'gists_url': 'https://api.github.com/users/necolas/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/necolas/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/necolas/subscriptions', 'organizations_url': 'https://api.github.com/users/necolas/orgs', 'repos_url': 'https://api.github.com/users/necolas/repos', 'events_url': 'https://api.github.com/users/necolas/events{/privacy}', 'received_events_url': 'https://api.github.com/users/necolas/received_events', 'type': 'User', 'site_admin': False, 'contributions': 92}, {'login': 'syranide', 'id': 1714255, 'node_id': 'MDQ6VXNlcjE3MTQyNTU=', 'avatar_url': 'https://avatars1.githubusercontent.com/u/1714255?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/syranide', 'html_url': 'https://github.com/syranide', 'followers_url': 'https://api.github.com/users/syranide/followers', 'following_url': 'https://api.github.com/users/syranide/following{/other_user}', 'gists_url': 'https://api.github.com/users/syranide/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/syranide/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/syranide/subscriptions', 'organizations_url': 'https://api.github.com/users/syranide/orgs', 'repos_url': 'https://api.github.com/users/syranide/repos', 'events_url': 'https://api.github.com/users/syranide/events{/privacy}', 'received_events_url': 'https://api.github.com/users/syranide/received_events', 'type': 'User', 'site_admin': False, 'contributions': 77}, {'login': 'cpojer', 'id': 13352, 'node_id': 'MDQ6VXNlcjEzMzUy', 'avatar_url': 'https://avatars0.githubusercontent.com/u/13352?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/cpojer', 'html_url': 'https://github.com/cpojer', 'followers_url': 'https://api.github.com/users/cpojer/followers', 'following_url': 'https://api.github.com/users/cpojer/following{/other_user}', 'gists_url': 'https://api.github.com/users/cpojer/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/cpojer/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/cpojer/subscriptions', 'organizations_url': 'https://api.github.com/users/cpojer/orgs', 'repos_url': 'https://api.github.com/users/cpojer/repos', 'events_url': 'https://api.github.com/users/cpojer/events{/privacy}', 'received_events_url': 'https://api.github.com/users/cpojer/received_events', 'type': 'User', 'site_admin': False, 'contributions': 70}, {'login': 'flarnie', 'id': 1114467, 'node_id': 'MDQ6VXNlcjExMTQ0Njc=', 'avatar_url': 'https://avatars2.githubusercontent.com/u/1114467?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/flarnie', 'html_url': 'https://github.com/flarnie', 'followers_url': 'https://api.github.com/users/flarnie/followers', 'following_url': 'https://api.github.com/users/flarnie/following{/other_user}', 'gists_url': 'https://api.github.com/users/flarnie/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/flarnie/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/flarnie/subscriptions', 'organizations_url': 'https://api.github.com/users/flarnie/orgs', 'repos_url': 'https://api.github.com/users/flarnie/repos', 'events_url': 'https://api.github.com/users/flarnie/events{/privacy}', 'received_events_url': 'https://api.github.com/users/flarnie/received_events', 'type': 'User', 'site_admin': False, 'contributions': 67}, {'login': 'koba04', 'id': 250407, 'node_id': 'MDQ6VXNlcjI1MDQwNw==', 'avatar_url': 'https://avatars2.githubusercontent.com/u/250407?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/koba04', 'html_url': 'https://github.com/koba04', 'followers_url': 'https://api.github.com/users/koba04/followers', 'following_url': 'https://api.github.com/users/koba04/following{/other_user}', 'gists_url': 'https://api.github.com/users/koba04/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/koba04/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/koba04/subscriptions', 'organizations_url': 'https://api.github.com/users/koba04/orgs', 'repos_url': 'https://api.github.com/users/koba04/repos', 'events_url': 'https://api.github.com/users/koba04/events{/privacy}', 'received_events_url': 'https://api.github.com/users/koba04/received_events', 'type': 'User', 'site_admin': False, 'contributions': 66}, {'login': 'aweary', 'id': 6886061, 'node_id': 'MDQ6VXNlcjY4ODYwNjE=', 'avatar_url': 'https://avatars2.githubusercontent.com/u/6886061?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/aweary', 'html_url': 'https://github.com/aweary', 'followers_url': 'https://api.github.com/users/aweary/followers', 'following_url': 'https://api.github.com/users/aweary/following{/other_user}', 'gists_url': 'https://api.github.com/users/aweary/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/aweary/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/aweary/subscriptions', 'organizations_url': 'https://api.github.com/users/aweary/orgs', 'repos_url': 'https://api.github.com/users/aweary/repos', 'events_url': 'https://api.github.com/users/aweary/events{/privacy}', 'received_events_url': 'https://api.github.com/users/aweary/received_events', 'type': 'User', 'site_admin': False, 'contributions': 66}, {'login': 'marocchino', 'id': 128431, 'node_id': 'MDQ6VXNlcjEyODQzMQ==', 'avatar_url': 'https://avatars3.githubusercontent.com/u/128431?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/marocchino', 'html_url': 'https://github.com/marocchino', 'followers_url': 'https://api.github.com/users/marocchino/followers', 'following_url': 'https://api.github.com/users/marocchino/following{/other_user}', 'gists_url': 'https://api.github.com/users/marocchino/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/marocchino/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/marocchino/subscriptions', 'organizations_url': 'https://api.github.com/users/marocchino/orgs', 'repos_url': 'https://api.github.com/users/marocchino/repos', 'events_url': 'https://api.github.com/users/marocchino/events{/privacy}', 'received_events_url': 'https://api.github.com/users/marocchino/received_events', 'type': 'User', 'site_admin': False, 'contributions': 45}, {'login': 'kohei-takata', 'id': 7623979, 'node_id': 'MDQ6VXNlcjc2MjM5Nzk=', 'avatar_url': 'https://avatars0.githubusercontent.com/u/7623979?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/kohei-takata', 'html_url': 'https://github.com/kohei-takata', 'followers_url': 'https://api.github.com/users/kohei-takata/followers', 'following_url': 'https://api.github.com/users/kohei-takata/following{/other_user}', 'gists_url': 'https://api.github.com/users/kohei-takata/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/kohei-takata/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/kohei-takata/subscriptions', 'organizations_url': 'https://api.github.com/users/kohei-takata/orgs', 'repos_url': 'https://api.github.com/users/kohei-takata/repos', 'events_url': 'https://api.github.com/users/kohei-takata/events{/privacy}', 'received_events_url': 'https://api.github.com/users/kohei-takata/received_events', 'type': 'User', 'site_admin': False, 'contributions': 39}, {'login': 'TheSavior', 'id': 249164, 'node_id': 'MDQ6VXNlcjI0OTE2NA==', 'avatar_url': 'https://avatars0.githubusercontent.com/u/249164?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/TheSavior', 'html_url': 'https://github.com/TheSavior', 'followers_url': 'https://api.github.com/users/TheSavior/followers', 'following_url': 'https://api.github.com/users/TheSavior/following{/other_user}', 'gists_url': 'https://api.github.com/users/TheSavior/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/TheSavior/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/TheSavior/subscriptions', 'organizations_url': 'https://api.github.com/users/TheSavior/orgs', 'repos_url': 'https://api.github.com/users/TheSavior/repos', 'events_url': 'https://api.github.com/users/TheSavior/events{/privacy}', 'received_events_url': 'https://api.github.com/users/TheSavior/received_events', 'type': 'User', 'site_admin': False, 'contributions': 30}, {'login': 'chicoxyzzy', 'id': 1507086, 'node_id': 'MDQ6VXNlcjE1MDcwODY=', 'avatar_url': 'https://avatars3.githubusercontent.com/u/1507086?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/chicoxyzzy', 'html_url': 'https://github.com/chicoxyzzy', 'followers_url': 'https://api.github.com/users/chicoxyzzy/followers', 'following_url': 'https://api.github.com/users/chicoxyzzy/following{/other_user}', 'gists_url': 'https://api.github.com/users/chicoxyzzy/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/chicoxyzzy/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/chicoxyzzy/subscriptions', 'organizations_url': 'https://api.github.com/users/chicoxyzzy/orgs', 'repos_url': 'https://api.github.com/users/chicoxyzzy/repos', 'events_url': 'https://api.github.com/users/chicoxyzzy/events{/privacy}', 'received_events_url': 'https://api.github.com/users/chicoxyzzy/received_events', 'type': 'User', 'site_admin': False, 'contributions': 29}, {'login': 'lunaruan', 'id': 2735514, 'node_id': 'MDQ6VXNlcjI3MzU1MTQ=', 'avatar_url': 'https://avatars0.githubusercontent.com/u/2735514?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/lunaruan', 'html_url': 'https://github.com/lunaruan', 'followers_url': 'https://api.github.com/users/lunaruan/followers', 'following_url': 'https://api.github.com/users/lunaruan/following{/other_user}', 'gists_url': 'https://api.github.com/users/lunaruan/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/lunaruan/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/lunaruan/subscriptions', 'organizations_url': 'https://api.github.com/users/lunaruan/orgs', 'repos_url': 'https://api.github.com/users/lunaruan/repos', 'events_url': 'https://api.github.com/users/lunaruan/events{/privacy}', 'received_events_url': 'https://api.github.com/users/lunaruan/received_events', 'type': 'User', 'site_admin': False, 'contributions': 29}, {'login': 'keyz', 'id': 2268452, 'node_id': 'MDQ6VXNlcjIyNjg0NTI=', 'avatar_url': 'https://avatars0.githubusercontent.com/u/2268452?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/keyz', 'html_url': 'https://github.com/keyz', 'followers_url': 'https://api.github.com/users/keyz/followers', 'following_url': 'https://api.github.com/users/keyz/following{/other_user}', 'gists_url': 'https://api.github.com/users/keyz/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/keyz/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/keyz/subscriptions', 'organizations_url': 'https://api.github.com/users/keyz/orgs', 'repos_url': 'https://api.github.com/users/keyz/repos', 'events_url': 'https://api.github.com/users/keyz/events{/privacy}', 'received_events_url': 'https://api.github.com/users/keyz/received_events', 'type': 'User', 'site_admin': False, 'contributions': 28}, {'login': 'rickhanlonii', 'id': 2440089, 'node_id': 'MDQ6VXNlcjI0NDAwODk=', 'avatar_url': 'https://avatars0.githubusercontent.com/u/2440089?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/rickhanlonii', 'html_url': 'https://github.com/rickhanlonii', 'followers_url': 'https://api.github.com/users/rickhanlonii/followers', 'following_url': 'https://api.github.com/users/rickhanlonii/following{/other_user}', 'gists_url': 'https://api.github.com/users/rickhanlonii/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/rickhanlonii/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/rickhanlonii/subscriptions', 'organizations_url': 'https://api.github.com/users/rickhanlonii/orgs', 'repos_url': 'https://api.github.com/users/rickhanlonii/repos', 'events_url': 'https://api.github.com/users/rickhanlonii/events{/privacy}', 'received_events_url': 'https://api.github.com/users/rickhanlonii/received_events', 'type': 'User', 'site_admin': False, 'contributions': 28}, {'login': 'mcsheffrey', 'id': 61091, 'node_id': 'MDQ6VXNlcjYxMDkx', 'avatar_url': 'https://avatars2.githubusercontent.com/u/61091?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/mcsheffrey', 'html_url': 'https://github.com/mcsheffrey', 'followers_url': 'https://api.github.com/users/mcsheffrey/followers', 'following_url': 'https://api.github.com/users/mcsheffrey/following{/other_user}', 'gists_url': 'https://api.github.com/users/mcsheffrey/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/mcsheffrey/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/mcsheffrey/subscriptions', 'organizations_url': 'https://api.github.com/users/mcsheffrey/orgs', 'repos_url': 'https://api.github.com/users/mcsheffrey/repos', 'events_url': 'https://api.github.com/users/mcsheffrey/events{/privacy}', 'received_events_url': 'https://api.github.com/users/mcsheffrey/received_events', 'type': 'User', 'site_admin': False, 'contributions': 26}, {'login': 'bgw', 'id': 180404, 'node_id': 'MDQ6VXNlcjE4MDQwNA==', 'avatar_url': 'https://avatars2.githubusercontent.com/u/180404?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/bgw', 'html_url': 'https://github.com/bgw', 'followers_url': 'https://api.github.com/users/bgw/followers', 'following_url': 'https://api.github.com/users/bgw/following{/other_user}', 'gists_url': 'https://api.github.com/users/bgw/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/bgw/starred{/owner}{/repo}', 'subscriptions_url': 'https://api.github.com/users/bgw/subscriptions', 'organizations_url': 'https://api.github.com/users/bgw/orgs', 'repos_url': 'https://api.github.com/users/bgw/repos', 'events_url': 'https://api.github.com/users/bgw/events{/privacy}', 'received_events_url': 'https://api.github.com/users/bgw/received_events', 'type': 'User', 'site_admin': False, 'contributions': 24}]

pie_plot(contributor_list)
