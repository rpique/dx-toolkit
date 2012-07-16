#!/usr/bin/env python

import os, sys, json, re

preamble = '''// Do not modify this file by hand.
//
// It is automatically generated by nucleus/bin/generateJSAPIWrappers.py.
// (Run make api_wrappers to update it.)

var dx = require('DNAnexus');
'''

class_method_template = '''
exports.{method_name} = function(input_params) {{
  return dx.DXHTTPRequest('{route}', input_params);
}};
'''

object_method_template = '''
exports.{method_name} = function(object_id, input_params) {{
  return dx.DXHTTPRequest('/' + object_id + '/{method_route}', input_params);
}};
'''

app_object_method_template = '''
exports.{method_name} = function(app_id_or_name, input_params) {{
  return dx.DXHTTPRequest('/' + app_id_or_name + '/{method_route}', input_params);
}};

exports.{method_name}WithAlias = function(app_name, app_alias, input_params) {{
  return exports.{method_name}(app_name + '/' + app_alias, input_params);
}};
'''

print preamble

for method in json.loads(sys.stdin.read()):
    route, signature, opts = method
    method_name = signature.split("(")[0]
    if (opts['objectMethod']):
        root, oid_route, method_route = route.split("/")
        if oid_route == 'app-xxxx':
            print app_object_method_template.format(method_name=method_name, method_route=method_route)
        else:
            print object_method_template.format(method_name=method_name, method_route=method_route)
    else:
        print class_method_template.format(method_name=method_name, route=route)