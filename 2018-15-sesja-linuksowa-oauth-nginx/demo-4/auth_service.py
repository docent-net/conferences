"""
This lightweight web service performs authentication. All requests that reach
this service should be proxied through nginx.

See: https://developers.google.com/api-client-library/python/auth/web-app
"""

from __future__ import print_function

import argparse
import base64
import codecs
import inspect
import os
import pprint
import json
import logging
import logging.handlers
import sys
import textwrap
import urllib
import zipfile

import flask
import jinja2
import oauth2client.client
import requests
import oauthsub

VERSION = '0.1.2'


class ZipfileLoader(jinja2.BaseLoader):

  def __init__(self, zipfile_path, directory):
    self.zip = zipfile.ZipFile(zipfile_path, mode='r')
    self.dir = directory

  def __del__(self):
    self.zip.close()

  def get_source(self, environment, template):
    # NOTE(josh): not os.path because zipfile uses forward slash
    tplpath = '{}/{}'.format(self.dir, template)
    with self.zip.open(tplpath, 'r') as infile:
      source = infile.read().decode('utf-8')

    return source, tplpath, lambda: True


def get_parent_path():
  """
  Return the parent path of the oauthsub package.
  """
  modpath = os.path.dirname(oauthsub.__file__)
  return os.path.dirname(modpath)


def is_zipfile():
  """
  Return true if we are running from a zipfile. This is determined to be the
  case if the __file__ of this module is in a zipfile.
  """
  modparent = get_parent_path()
  logging.debug("module parent path is %s", modparent)
  return os.path.exists(modparent) and zipfile.is_zipfile(modparent)


class Application(object):
  """
  Main application context. Exists as a class to keep things local... even
  though flask is all about the global state.
  """

  def __init__(self, config):
    """Configure jinja, beaker, etc."""
    self.config = config

    if is_zipfile():
      logging.info('Using ZipfileLoader for templates')
      template_loader = ZipfileLoader(get_parent_path(), 'oauthsub/templates')
    else:
      logging.info('Using PackageLoader for templates')
      template_loader = jinja2.PackageLoader('oauthsub', 'templates')
    self.jinja = jinja2.Environment(loader=template_loader)
    self.jinja.globals.update(url_encode=urllib.quote_plus)

    self.flask = flask.Flask(__name__)
    self.flask.secret_key = config.flask_privkey
    self.flask.debug = self.config.flask_debug
    for key, value in config.flaskopt.items():
      self.flask.config[key] = value

    self.flask.add_url_rule(config.route_prefix, 'hello', self.hello)
    self.flask.add_url_rule('{}/login'.format(config.route_prefix),
                            'login', self.callback)
    self.flask.add_url_rule('{}/logout'.format(config.route_prefix),
                            'logout', self.logout)
    self.flask.add_url_rule('{}/callback'.format(config.route_prefix),
                            'callback', self.callback)
    self.flask.add_url_rule('{}/get_session'.format(config.route_prefix),
                            'get_session', self.get_session)
    self.flask.add_url_rule('{}/query_auth'.format(config.route_prefix),
                            'query_auth', self.query_auth)
    self.flask.add_url_rule('/public/401', 'forbidden', self.forbidden)

  def run(self, *args, **kwargs):
    """Just runs the flask app."""
    self.flask.run(*args, **kwargs)

  def render_message(self, message, *args, **kwargs):
    # pylint: disable=no-member
    return self.jinja.get_template('message.html.tpl').render(
        session=flask.session, message=message.format(*args, **kwargs))

  def hello(self):
    """A more or less empty endpoint."""

    # pylint: disable=no-member
    return self.jinja.get_template('message.html.tpl').render(
        session=flask.session, message='Hello')

  def query_auth(self):
    """
    This is the main endpoint used by nginx to check authorization. If this
    is an nginx request the X-Original-URI will be passed as an http header.
    """
    original_uri = flask.request.headers.get('X-Original-URI')
    if original_uri:
      logging.debug('Doing auth for original URI: %s, session %s',
                    original_uri, flask.session.get('id', None))

      # NOTE(josh): we don't do any whitelisting here, we'll let the nginx
      # config decide which urls to reqest auth for
      if flask.session.get('oauthsub-user', None) is not None:
        response = flask.make_response("", 200, {})
        if self.config.response_header:
          response.headers[self.config.response_header] \
              = flask.session.get('oauthsub-user')
        return response
      else:
        # NOTE(josh): since nginx will return a 401, it will not pass the
        # Set-Cookie header to the client. This session will not be associated
        # with the client unless they already have a cookie for this site.
        # There's not much point in dealing with the X-Original-URI here since
        # we can't realiably maintain any context.
        return flask.make_response("", 401, {})
    else:
      flask.abort(401)

  def forbidden(self):
    """
    The page served when a user isn't authorized. We'll just set the return
    path if it's available and then kick them through oauth2.
    """
    original_uri = flask.request.headers.get('X-Original-URI')
    logging.info('Serving forbidden, session %s, original uri: %s',
                 flask.session.get('id', None), original_uri)

    # NOTE(josh): it seems we can't do a redirect from the 401 page, or else it
    # might be on the browser side, but we get stuck at some google text saying
    # that the page should automatically redirect but it doesn't. Let's just
    # print the message and let them login. If they login it will return them
    # to where they wanted to go in the first place.
    return self.render_message('Permission denied. Are you logged in?')

  def get_flow(self):
    """
    Return the oauth2client flow object
    """

    redirect_uri = '{}{}/callback'.format(self.config.rooturl,
                                          self.config.route_prefix)
    original_uri = flask.request.args.get('original_uri', None)
    if original_uri is not None:
      redirect_uri += '?' + urllib.urlencode(dict(original_uri=original_uri))

    # Construct a 'flow' which helps us step through the oauth handshake
    # A "flow" is a google provided API which helps us step through the
    return oauth2client.client.flow_from_clientsecrets(
        self.config.secrets,
        scope='https://www.googleapis.com/auth/userinfo.email',
        redirect_uri=redirect_uri)

  def session_get(self, key, default=None):
    """
    Return the value of the session variable `key`, using the prefix-qualifed
    name for `key`
    """
    qualified_key = '{}{}'.format(self.config.session_key_prefix, key)
    return flask.session.get(qualified_key, default)

  def session_set(self, key, value):
    """
    Set the value of the session variable `key`, using the prefix-qualifed
    name for `key`
    """
    qualified_key = '{}{}'.format(self.config.session_key_prefix, key)
    flask.session[qualified_key] = value

  def login(self):
    """
    The login page. Start of the oauth dance. Construct a flow, get redirect,
    bounce the user.
    """

    if self.session_get('user') is not None:
      return self.render_message("You are already logged in as {}",
                                 self.session_get('user'))

    flow = self.get_flow()
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)

  def callback(self):
    """
    Handle oauth bounce-back.
    """

    # If we didn't received a 'code' in the query parameters then this
    # definately not a redirect back from google.  Assume this is a user meaning
    # to use the /login endpoint and punt them to the start of the dance.
    if 'code' not in flask.request.args:
      return self.login()

    flow = self.get_flow()
    auth_code = flask.request.args.get('code')

    # Exchange the code that google gave us for an actual credentials object,
    # and store those credentials in the session for this user.

    # NOTE(josh): We don't actually do anything persistent with the credentials
    # right now, other than to store them as a certificate that the user is
    # authenticated. In the normal use case we would need access to the
    # credentials in the future in order to hit google API's on behalf of the
    # user.
    credentials = flow.step2_exchange(auth_code)

    # Use the credentials that we have in order to get the users information
    # from google. We only need one request to get the user's email address
    # and name.
    request_url = ('https://www.googleapis.com/userinfo/v2/me?alt=json'
                   '&&access_token={}'.format(credentials.access_token))
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json; charset=UTF-8'}
    response = requests.get(request_url, headers=headers)

    if response.status_code != 200:
      message = 'Failed to query googleapis: [{}]'.format(response.status)
      return flask.make_response(self.render_message(message), 500, {})

    # We'll store the users email, name, and 'given_name' from google's
    # reponse. This is just to help the user understand which google identity
    # they currently have activated.
    parsed_content = json.loads(response.content)

    for key in ['email', 'name', 'given_name']:
      if key in parsed_content:
        self.session_set(key, parsed_content[key])
      else:
        self.session_set(key, 'unknown')

    if 'email' not in parsed_content:
      content = self.render_message("Login error, google did not tell us"
                                    " your email address!")
      return flask.make_response(content, 500, {})

    # If the user logged in with an email domain other than <??> the we want
    # to warn them that they are probably not doing what they wanted to do.
    if parsed_content.get('hd') not in self.config.allowed_domains:
      content = self.render_message('You did not login with the right account!')
      return flask.make_response(content, 401, {})

    # At this point the user is authed
    self.session_set('credentials', credentials.to_json())
    self.session_set('user', parsed_content['email'].rsplit('@', 1)[0])

    # If we are logging-in due to attempt to access an auth-requiring page,
    # then go to back to that page
    original_uri = flask.request.args.get('original_uri', None)
    if original_uri is None:
      logging.info('Finished auth, no original_uri in request')
      return flask.redirect(self.config.rooturl)

    logging.debug('Finished auth, redirecting to: %s', original_uri)
    return flask.redirect(self.config.rooturl + original_uri)

  def logout(self):
    """
    Delete the user's session, effectively logging them out.
    """
    flask.session.clear()
    return self.render_message('Logged out')

  def get_session(self):
    """
    Return the user's session as a json object. Can be used to retrieve user
    identity within other frontend services, or for debugging.
    """

    session_dict = {key: self.session_get(key)
                    for key in ['email', 'name', 'given_name', 'user']}
    return flask.jsonify(session_dict)


def get_default(obj, default):
  """
  If obj is not `None` then return it. Otherwise return default.
  """
  if obj is None:
    return default

  return obj


class Configuration(object):
  """
  Simple configuration object. Holds named members for different configuration
  options. Can be serialized to a dictionary which would be a valid kwargs
  for the constructor.
  """

  # pylint: disable=too-many-arguments
  def __init__(self, rooturl=None, secrets=None,
               flask_debug=False, flask_privkey=None, response_header=None,
               allowed_domains=None, host=None, port=None, logdir=None,
               flaskopt=None, route_prefix=None, session_key_prefix=None,
               **kwargs):
    self.rooturl = get_default(rooturl, 'http://localhost')
    self.secrets = get_default(secrets, '/tmp/client_secrets.json')
    self.flask_debug = flask_debug
    self.flask_privkey = get_default(flask_privkey,
                                     base64.b64encode(os.urandom(24)))
    self.response_header = response_header
    self.allowed_domains = get_default(allowed_domains, ['gmail.com'])
    self.host = get_default(host, '0.0.0.0')
    self.port = get_default(port, 8081)
    self.logdir = get_default(logdir, '/tmp/oauthsub/logs')
    self.flaskopt = get_default(flaskopt, {
        'SESSION_TYPE': 'filesystem',
        'SESSION_FILE_DIR': '/tmp/oauthsub/session_data',
        'PERMANENT_SESSION_LIFETIME': 864000
    })
    self.route_prefix = get_default(route_prefix, '/auth')
    self.session_key_prefix = get_default(session_key_prefix, 'oauthsub-')

    for key, _ in kwargs.items():
      if not key.startswith('__'):
        logging.warn("Ignoring extra configuration option %s", key)

  @classmethod
  def get_fields(cls):
    """
    Return a list of field names in constructor order.
    """
    return inspect.getargspec(cls.__init__).args[1:]

  def serialize(self):
    """
    Return a dictionary describing the configuration.
    """
    return {field: getattr(self, field)
            for field in self.get_fields()}


def parse_bool(string):
  """
  Parse a string into a boolean.
  """

  if string.lower() in ('y', 'yes', 't', 'true', '1', 'yup', 'yeah', 'yada'):
    return True
  elif string.lower() in ('n', 'no', 'f', 'false', '0', 'nope', 'nah', 'nada'):
    return False

  logging.warn("Ambiguous truthiness of string '%s' evalutes to 'FALSE'",
               string)
  return False


VARDOCS = {
    'rooturl': 'The root URL for browser redirects',
    'secrets': 'The location of client_secrets.json',
    'flask_debug': 'Enable flask debugging for testing',
    'flask_privkey': 'Secret key used to sign cookies',
    'response_header': "If specified, the authenticated user's ``username`` "
                       "will be passed as a response header with this key.",
    'allowed_domains': "List of domains that we allow in the `hd` field of the"
                       "google response. Set this to your company gsuite "
                       "domains.",
    'host': "The address to listening on",
    'port': "The port to listen on",
    'logdir': "Directory where we store resource files",
    'flaskopt': "Flask configuration options. Set session config here.",
    'route_prefix': "All flask routes (endpoints) are prefixed with this",
    'session_key_prefix': "All session keys are prefixed with this"
}


def dump_config(config, outfile):
  """
  Dump configuration to the output stream
  """
  ppr = pprint.PrettyPrinter(indent=2)
  for key in Configuration.get_fields():
    helptext = VARDOCS.get(key, None)
    if helptext:
      for line in textwrap.wrap(helptext, 78):
        outfile.write('# ' + line + '\n')
    value = getattr(config, key)
    if isinstance(value, dict):
      outfile.write('{} = {}\n\n'.format(key, json.dumps(value, indent=2)))
    else:
      outfile.write('{} = {}\n\n'.format(key, ppr.pformat(value)))


def main():
  format_str = '%(levelname)-4s %(filename)s [%(lineno)-3s] : %(message)s'
  logging.basicConfig(level=logging.DEBUG,
                      format=format_str,
                      datefmt='%Y-%m-%d %H:%M:%S',
                      filemode='w')

  parser = argparse.ArgumentParser(prog='oauthsub', description=__doc__)
  parser.add_argument('--dump-config', action='store_true',
                      help='Dump configuration and exit')
  parser.add_argument('-v', '--version', action='version', version=VERSION)
  parser.add_argument('-l', '--log-level', default='info',
                      choices=['debug', 'info', 'warning', 'error'],
                      help='Increase log level to include info/debug')
  parser.add_argument('-c', '--config-file',
                      help='use a configuration file')

  config_dict = Configuration().serialize()
  for key in Configuration.get_fields():
    value = config_dict[key]
    helptext = VARDOCS.get(key, None)
    # NOTE(josh): argparse store_true isn't what we want here because we want
    # to distinguish between "not specified" = "default" and "specified"
    if isinstance(value, bool):
      parser.add_argument('--' + key.replace('_', '-'), nargs='?', default=None,
                          const=True, type=parse_bool, help=helptext)
    elif isinstance(value, (str, unicode, int, float)) or value is None:
      parser.add_argument('--' + key.replace('_', '-'), type=type(value),
                          help=helptext)
    # NOTE(josh): argparse behavior is that if the flag is not specified on
    # the command line the value will be None, whereas if it's specified with
    # no arguments then the value will be an empty list. This exactly what we
    # want since we can ignore `None` values.
    elif isinstance(value, (list, tuple)):
      parser.add_argument('--' + key.replace('_', '-'), nargs='*',
                          help=helptext)
  args = parser.parse_args()

  if args.dump_config:
    dump_config(Configuration(), sys.stdout)
    sys.exit(0)

  if args.config_file:
    configpath = os.path.expanduser(args.config_file)
    with codecs.open(configpath, 'r', encoding='utf8') as infile:
      # pylint: disable=W0122
      exec(infile.read(), config_dict)

  for key, value in vars(args).items():
    if key in config_dict and value is not None:
      config_dict[key] = value
  config = Configuration(**config_dict)

  # Create directory for logs if it doesn't exist
  if not os.path.exists(config.logdir):
    os.makedirs(config.logdir)

  # We'll add a handler which puts log events in an actual file for review as
  # needed. We'll put the log file on a rotation where each log may grow up to
  # 1 megabyte with up to 10 backups
  filelog = logging.handlers.RotatingFileHandler(
      os.path.join(config.logdir, 'oauthsub.log'),
      maxBytes=int(1e6), backupCount=10)

  # We'll add a timestamp to the format for this log
  format_str = ('%(asctime)s %(levelname)-4s %(filename)s [%(lineno)-3s] :'
                ' %(message)s')
  filelog.setFormatter(logging.Formatter(format_str))
  logging.getLogger('').addHandler(filelog)

  config_dict = config.serialize()
  config_dict.pop('secrets')
  logging.info('Configuration: %s', json.dumps(config_dict, indent=2))

  # NOTE(josh): hack to deal with jinja's failure to resolve relative imports
  # to absolute paths
  oauthsub.__file__ = os.path.abspath(oauthsub.__file__)
  app = Application(config)
  app.run(threaded=True, host=config.host, port=config.port)
