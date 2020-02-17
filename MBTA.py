from HTTPHandler import *

class MBTA:
    routesURL = 'https://api-v3.mbta.com/routes'
    routesParams = {'filter[type]':'0,1',
              'fields[route]':'long_name',
              }
    stopsURL = 'https://api-v3.mbta.com/stops'
    request = None
    routes = None
    stops = {}
    stopToRoutesDict = dict()
    routeConnectionDict = dict()

    def __init__(self):
        self.request = HTTPHandler()


    def getRoutes(self):
        response = self.request.makeHttpConnection(self.routesURL, self.routesParams)
        if response is not None:
            self.routes =  response['data']
        else:
            print("Fail to get routes")

    def getStops(self):
        for route in self.routes:
            stopsParams = {'filter[route]': route['id'],
              'fields[stop]':'name',
              }
            response = self.request.makeHttpConnection(self.stopsURL, stopsParams)
            if response is not None:
                self.stops[route['attributes']['long_name']] = response['data']
            else:
                print(f'Fail to get stops for: {route["attributes"]["long_name"]}')

    def printMaxStops(self):
        maxCount = 0
        maxRoute = "None"
        for key, value in self.stops.items():
            if len(value)> maxCount:
                maxCount = len(value)
                maxRoute = key
            elif len(value) == maxCount:
                maxRoute = maxRoute + "," + key
            else:
                continue
        print(f'Route with most stops: {maxRoute}. The number of stops: {maxCount}')


    def printMinStops(self):
        minCount = 1000 #assume the min route has less than 1000 stops
        minRoute = "None"
        for key,value in self.stops.items():
            if len(value)<minCount:
                minCount = len(value)
                minRoute = key
            elif len(value) == minCount:
                minRoute = minRoute + "," + key
            else:
                continue
        print(f'Route with least stops: {minRoute}. The number of stops: {minCount}')

    def setStopRouteDict(self):
        for key, value in self.stops.items():
            for stop in value:
                stopName = stop['attributes']['name']
                if stopName in self.stopToRoutesDict: #add the route name to the list if it is already stop is present
                    self.stopToRoutesDict[stopName].add(key)
                else:
                    self.stopToRoutesDict[stopName] = {key} #add the route

    def printCommonStops(self):
        """"make routeConnectionDict and print the connecting stops"""
        self.setStopRouteDict()
        for key, value in self.stopToRoutesDict.items():
            if len(value) > 1:
                for route in value:
                    if route in self.routeConnectionDict:
                        self.routeConnectionDict[route].update(value.copy())
                    else:
                        self.routeConnectionDict[route] = value.copy()
                print(f'Connecting stop: {key} for routes: {value}')
            else:
                continue

    def findRouteToTravel(self, startStop, endStop):
        if(len(startStop) == 0 or len(endStop) == 0):
            print("Invaild Inputs")
            return
        startRoute = self.stopToRoutesDict[startStop]
        endRoute = self.stopToRoutesDict[endStop]
        result = self.findRouteToTravelHelper(startRoute,endRoute,set())
        print(result)


    def findRouteToTravelHelper(self,startRouteSet,endRouteSet, visitedRouteSet):
        for routeStart in startRouteSet: #base case
            if routeStart in endRouteSet:
                return[routeStart]
        #remove the visited routes from startRouteSet
        for routeStart in startRouteSet:
            if routeStart not in visitedRouteSet:
                visitedRouteSet.add(routeStart)
                result = self.findRouteToTravelHelper(self.routeConnectionDict[routeStart],endRouteSet,visitedRouteSet)
                if len(result)!= 0: # if the result is not empty
                    for i in range(0, len(result)):#check if the route is available to
                        if result[i] in startRouteSet:
                            return result[0:i+1]
                    result.append(routeStart)
                    return result
        return []



    def displayRoutes(self):
        #print the routes in long names
        print("MBTA routes:")
        for route in self.routes:
            print(route['attributes']['long_name'])


if __name__ == '__main__':
    test = MBTA()
    test.getRoutes()# I choose to rely on the server API to filter the results, Because it avoids a lot of unwanted data.
    test.displayRoutes()
    test.getStops()
    test.printMaxStops()
    test.printMinStops()
    test.printCommonStops()
    test.findRouteToTravel("Davis","Bowdoin")#[blue,green,red]
    test.findRouteToTravel("", "")
    test.findRouteToTravel("Ashmont", "Arlington")