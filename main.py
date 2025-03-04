from TweetterParser import TwitterParser
from files_management import check_content

projects = ["starknet"]
parser = TwitterParser()
for project in projects:
    parser.parse_project_tweets(project)
    check_content(project)