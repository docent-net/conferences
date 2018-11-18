# The root URL for browser redirects
rooturl = 'http://sesja-4.demo.com'

# The location of client_secrets.json
secrets = '/srv/client_secrets.json'

# Enable flask debugging for testing
flask_debug = True

# Secret key used to sign cookies
flask_privkey = 'XXXXYYYYY'

# If specified, the authenticated user's ``username`` will be passed as a
# response header with this key.
response_header = None

# List of domains that we allow in the `hd` field of thegoogle response. Set
# this to your company gsuite domains.
allowed_domains = ['lasyk.info']

# The address to listening on
host = '127.0.0.1'

# The port to listen on
port = 8081

# Directory where we store resource files
logdir = '/srv/oauthsub/logs'

# Flask configuration options. Set session config here.
flaskopt = {
  "SESSION_FILE_DIR": "/srv/oauthsub/session_data",
  "PERMANENT_SESSION_LIFETIME": 864000,
  "SESSION_TYPE": "filesystem"
}