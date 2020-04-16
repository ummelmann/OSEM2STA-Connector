import requests
import os.path

api_functions = [
    "Datastreams",
    "FeaturesOfInterest",
    "HistoricalLocations",
    "Locations",
    "Observations",
    "ObservedProperties",
    "Sensors",
    "Things"
]

def top(list, count):
    newList = []
    if len(list) >= count:
        for i in range(count):
            newList.append(list[i])
    return (newList)

def select(dictionary: dict, selectionClauses: str):
    selectionClauseList = selectionClauses.split(',')
    newDictionary = {}
    for selectionClause in selectionClauseList:
        if selectionClause in dictionary:
            newDictionary[selectionClause] = dictionary[selectionClause]
    print(newDictionary)
    return(newDictionary)


def get_osem_boxes_as_sta_things(host_url: str, function_url: str):
    resp = requests.get('https://api.opensensemap.org/boxes')
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /boxes/ {}'.format(resp.status_code))

    sta_things = []
    osmboxes = resp.json()
    for osmbox in osmboxes:
        sta_from_osem = {'name': osmbox['name'],
                          'description': '',
                           'properties': {'exposure': osmbox['exposure'],
                                          'model': osmbox['model'],
                                          'createdAt': osmbox['createdAt']
                                          },
                           '@iot.id': osmbox['_id'],
                            '@iot.selfLink': host_url + function_url + '(\'' + osmbox['_id'] + '\')'
                        }
        if 'updatedAt' in osmbox:
            sta_from_osem['properties'].update({'updatedAt': osmbox['updatedAt']})
        if 'grouptag' in osmbox:
            sta_from_osem['properties'].update({'grouptag': osmbox['grouptag']})
        sta_things.append(sta_from_osem)


    return {'value': sta_things}

def get_osem_box_as_sta_thing(box_id: str, host_url: str, function_url: str):
    resp = requests.get('https://api.opensensemap.org/boxes/' + box_id)
    print(resp.url)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /boxes/ {}'.format(resp.status_code))

    osmbox= resp.json()

    sta_from_osem = {'name': osmbox['name'],
                     'description': '',
                     'properties': {'exposure': osmbox['exposure'],
                                    'model': osmbox['model'],
                                    'createdAt': osmbox['createdAt']
                                   },
                     'Datastreams @ iot.navigationLink': host_url + function_url + '/Datastreams',
                     '@iot.id': osmbox['_id'],
                     '@iot.selfLink': host_url + function_url
                    }

    if 'updatedAt' in osmbox:
        sta_from_osem['properties'].update({'updatedAt': osmbox['updatedAt']})
    if 'grouptag' in osmbox:
        sta_from_osem['properties'].update({'grouptag': osmbox['grouptag']})


    return (sta_from_osem)

def get_osem_boxes_as_sta_datastreams(host_url: str, function_url: str):
    resp = requests.get('https://api.opensensemap.org/boxes/')
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /boxes/ {}'.format(resp.status_code))

    sta_datastreams = []

    osmboxes= resp.json()
    for osmbox in osmboxes:
        sensors= osmbox['sensors']

        for sensor in sensors:
            if 'title' in sensor:
              sta_from_osem = {'name': sensor['title'],
                             'description': '',
                             "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                             'unitOfMeasurement': {'name': '',
                                                   'symbol': sensor['unit'],
                                                   'definition': ''
                                                 },
                          'Datastreams @ iot.navigationLink': host_url + function_url,
                          '@iot.id': osmbox['_id'] + ':' + sensor['_id'],
                          '@iot.selfLink': host_url + function_url + '(\'' + osmbox['_id'] + ':' + sensor['_id'] + '\')'
                          }
              sta_datastreams.append(sta_from_osem)

    return {'value': sta_datastreams}

def get_osem_box_as_sta_datastreams(box_id: str, host_url: str, function_url: str):
    resp = requests.get('https://api.opensensemap.org/boxes/' + box_id)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /boxes/ {}'.format(resp.status_code))

    base_url = os.path.split(function_url)[0]
    sta_datastreams = []
    osmbox= resp.json()
    sensors= osmbox['sensors']

    for sensor in sensors:
        if 'title' in sensor:
            sta_from_osem = {'name': sensor['title'],
                             'description': '',
                             "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                             'unitOfMeasurement': {'name': '',
                                                   'symbol': sensor['unit'],
                                                   'definition': ''
                                                 },
                          'Sensor@iot.navigationLink': host_url + base_url + '/Datastreams' + '(\'' + osmbox['_id'] + ':' + sensor['_id'] + '\')' + '/Sensor',
                          'Thing@iot.navigationLink': host_url + base_url + '/Datastreams' + '(\'' + osmbox['_id'] + ':' + sensor['_id'] + '\')' + '/Thing',
                          'Observations@iot.navigationLink': host_url + base_url + '/Datastreams' + '(\'' + osmbox['_id'] + ':' + sensor['_id'] + '\')' + '/Observations',
                          '@iot.id': osmbox['_id'] + ':' + sensor['_id'],
                          '@iot.selfLink': host_url + base_url + '/Datastreams' + '(\'' + osmbox['_id'] + ':' + sensor['_id'] + '\')'
                          }
            sta_datastreams.append(sta_from_osem)

    return {'value': sta_datastreams}

def get_osem_box_and_sensor_as_sta_datastream(sensor_box_id: str, host_url: str, function_url: str):
    sensor_box_id_array = sensor_box_id.split(":")
    resp = requests.get('https://api.opensensemap.org/boxes/' + sensor_box_id_array[0])

    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /boxes/ {}'.format(resp.status_code))

    osmbox= resp.json()
    sensors= osmbox['sensors']

    for sensor in sensors:
        if sensor['_id'] == sensor_box_id_array[1]:
            sta_from_osem = {'name': sensor['title'],
                           'description': '',
                           'observationType': "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                           'Sensor@iot.navigationLink': host_url + function_url + '/Sensor',
                           'Thing@iot.navigationLink': host_url + function_url + '/Thing',
                           'Observations@iot.navigationLink': host_url + function_url + '/Observations',
                           'unitOfMeasurement': {'name': '',
                                                 'symbol': sensor['unit'],
                                                 'definition': ''
                                                 },
                           'ObservedProperty@iot.navigationLink': host_url + function_url + 'ObservedProperty',
                           '@iot.id': sensor_box_id,
                           '@iot.selfLink': host_url + function_url
                           }

    return sta_from_osem

def get_osem_measurement_as_sta_observation(sensor_box_id: str, host_url: str, function_url: str, args):
    print(args)
    sensor_box_id_array = sensor_box_id.split(":")
    print('https://api.opensensemap.org/boxes/' + sensor_box_id_array[0] + '/data/' + sensor_box_id_array[1])
    resp = requests.get('https://api.opensensemap.org/boxes/' + sensor_box_id_array[0] + '/data/' + sensor_box_id_array[1])

    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /boxes/ {}'.format(resp.status_code))

    measurements = resp.json()

    sta_observations = []

    for measurement in measurements:
        sta_from_osem = {'phenomenonTime': None,
                         'resultTime': measurement['createdAt'],
                         'result': measurement['value'],
                         'Datastream@iot.navigationLink': host_url + function_url + '/Thing',
                         'FeatureOfInterest@iot.navigationLink': host_url + function_url + '/Observations',
                         '@iot.id': sensor_box_id,
                         '@iot.selfLink': host_url + function_url
                         }
        sta_observations.append(sta_from_osem)

    if args['top'] != 0:
        sta_observations = top(sta_observations, args['top'])

    if args['select'] != "":
        selected_sta_observations = []
        for sta_observation in sta_observations:
            selected_sta_observations.append(select(sta_observation, args['select']))
        sta_observations = selected_sta_observations

    return {'value': sta_observations}