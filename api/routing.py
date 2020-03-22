import openrouteservice

class Routing:

    def __init__(self):
        self.client = openrouteservice.Client(key='5b3ce3597851110001cf6248834ab776faae40c29d93aacafa5b3e6e')

    #coordinates are required in format ((8.34234,48.23424),(8.34423,48.26424), (8.34523,48.24424), (8.41423,48.21424))
    def calculate_route(self, coordinates):
        routes = self.client.directions(coordinates, profile='cycling-regular', optimize_waypoints=True)
        return routes

if __name__ == '__main__':
    coordinates = ((8.34234,48.23424),(8.34423,48.26424), (8.34523,48.24424), (8.41423,48.21424))
    r = Routing()
    routes = r.calculate_route(coordinates)
    print(routes)