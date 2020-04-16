from flask import request, url_for, Blueprint
from flask_cors import CORS
from flask_api import FlaskAPI, status, exceptions
import sta2osem
import os.path

theme = Blueprint(
    'flask-api', __name__,
    url_prefix='/flask-api',
    template_folder='templates', static_folder='static'
)

app = FlaskAPI(__name__)
app.blueprints['flask-api'] = theme

CORS(app)

api_functions = [
    'sta2osem',
    'osem2sta'
]

def api_functions_repr_url_extender(last_url, host_url):
    last_url_split = last_url.rsplit('/')
    url_extension = ""
    if len(last_url_split) > len(host_url) or last_url_split[-1] != "":
        copy_parts = len(last_url_split) - len(host_url) + 1
        for i in range(copy_parts):
            url_extension = url_extension + "/" + last_url_split[(i+1)*(-1)]
        return url_extension
    else:
        len(last_url_split) == len(host_url)
        return url_extension


def api_functions_repr(apifunction: str, key: str, prefix=''):
    url_ext = api_functions_repr_url_extender(request.url, request.host_url.rsplit('/'))
    return {
        'name': key,
        'url': request.host_url.rstrip('/') + prefix + url_for(apifunction, key=key)
    }


@app.route("/", methods=['GET'])
def api_function_list():
    """
    List or create notes.
    """
    # request.method == 'GET'
    return [api_functions_repr('api_function_list_detail', fnctx) for fnctx in api_functions]


@app.route("/<string:key>/v1", methods=['GET'])
def api_function_list_detail(key):
    """
    List or create notes.
    """
    # request.method == 'GET'
    if key == 'sta2osem':
        return [api_functions_repr('sta2osem_list', fnctx) for fnctx in sta2osem.api_functions]
    else:
        return [api_functions_repr('osem2stan_list', fnctx) for fnctx in api_functions]


@app.route("/sta2osem/v1/<string:key>", methods=['GET'])
def sta2osem_list(key):
    """
    List API-Functions from the SensorThings API which are mapped to the openSenseMap API
    """
    # request.method == 'GET'
    return [api_functions_repr('sta2osem_list', fnctx) for fnctx in sta2osem.api_functions]


@app.route("/sta2osem/v1/Things")
def sta2osem_things():
    return sta2osem.get_osem_boxes_as_sta_things(request.host_url.rstrip('/'), request.path)


@app.route("/sta2osem/v1/Things<string:key>")
def sta2osem_thing(key):
    return sta2osem.get_osem_box_as_sta_thing(key.strip('(\')'), request.host_url.rstrip('/'), request.path)


@app.route("/sta2osem/v1/Things<string:key>/Datastreams")
def sta2osem_thing_datastream(key):
    request_path = request.path
    split_path = os.path.split(request_path)
    print(split_path)
    origin_path = os.path.split(split_path[0])
    function_path = origin_path[0] + '/' + 'Datastreams' + key
    print('Path: ' + function_path)
    return sta2osem.get_osem_box_as_sta_datastreams(key.strip('(\')'), request.host_url.rstrip('/'), function_path)


@app.route("/sta2osem/v1/Datastreams")
def sta2osem_datastreams():
    return sta2osem.get_osem_boxes_as_sta_datastreams(request.host_url.rstrip('/'), request.path)


@app.route("/sta2osem/v1/Datastreams<string:key>")
def sta2osem_datastream(key):
    return sta2osem.get_osem_box_and_sensor_as_sta_datastream(key.strip('(\')'), request.host_url.rstrip('/'), request.path)


# TODO: Add Function for finding Sensor to Datastream
@app.route("/sta2osem/v1/Datastreams<string:key>/Sensor")
def sta2osem_datastream_sensor(key):
    return {}


@app.route("/sta2osem/v1/Datastreams<string:key>/Thing")
def sta2osem_datastream_thing(key):
    sensor_box_id = key.strip('(\')')
    sensor_box_id_array = sensor_box_id.split(":")
    box_id = sensor_box_id_array[0]
    request_path = request.path
    split_path = os.path.split(request_path)
    origin_path = os.path.split(split_path[0])
    function_path = origin_path[0] + '/' + 'Things' + '(\'' + box_id + '\')'
    return sta2osem.get_osem_box_as_sta_thing(box_id, request.host_url.rstrip('/'), function_path)


@app.route("/sta2osem/v1/Datastreams<string:key>/Observations")
def sta2osem_datastream_observations(key):
    args = {'top': request.args.get('$top', default=0, type=int),
            'select': request.args.get('$select', default="", type=str)
           }
    sensor_box_id = key.strip('(\')')
    sensor_box_id_array = sensor_box_id.split(":")
    box_id = sensor_box_id_array[0]
    request_path = request.path
    split_path = os.path.split(request_path)
    origin_path = os.path.split(split_path[0])
    function_path = origin_path[0] + '/' + 'Observations' + key
    return sta2osem.get_osem_measurement_as_sta_observation(key.strip('(\')'), request.host_url.rstrip('/'), function_path, args)

# TODO: Add Function for finding ObservedProperty to Datastream
@app.route("/sta2osem/v1/Datastreams<string:key>/ObservedProperty")
def sta2osem_datastream_observedproperty(key):
    return {}


if __name__ == "__main__":
    app.run(debug=True)
