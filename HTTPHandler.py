import requests
from requests.exceptions import HTTPError
import json

class HTTPHandler:


    def __int__(self):
        pass

    def makeHttpConnection(self, url, parameters):
    # making http connections with given url and parameters, return parsed result
        try:
            response = requests.get(url = url ,params=parameters)
            response.raise_for_status()
        except HTTPError as http_err: #print the errors
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response.json() #return the response

        return None # if get error return None



if __name__ == '__main__':
    url = 'https://api-v3.mbta.com/routes?'
    params = {'filter[type]': '0,1',
              'fields[route]':'long_name',
              }
    requests1 = HTTPHandler()
    responses = requests1.makeHttpConnection(url,params)
    print(responses)