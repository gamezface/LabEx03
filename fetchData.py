import requests
import os
import errno
import json
import sys
from string import Template

headers = {'Authorization': f'Bearer {sys.argv[1]}'} #sys.argv[1] = API_KEY

def runQuery(query, headers): 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception(f"Query failed to run by returning code of {request.status_code}.")

query = """
  query { 
    search(query: "stars:>100 language:Javascript", type: REPOSITORY, first: 100) {
      nodes {
        ... on Repository {
          createdAt
          openIssues: issues(states: [OPEN]) {
            totalCount
          }
          closedIssues: issues(states: [CLOSED]) {
            totalCount
          }
          url
          name
        }
      }
      pageInfo {
        endCursor
        hasNextPage
      }
    }
  }
"""
filename = 'output.json'
with open(filename, 'w') as file:
  json.dump([node for node in runQuery(query, headers)['data']['search']['nodes']], file)

print(f"Written to file {filename}")
