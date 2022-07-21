import urllib.request
import json
from jose import jwt


def decode(idToken):

    target_audience = "ambient-future-298121"

    certificate_url = 'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'

    response = urllib.request.urlopen(certificate_url)
    certs = response.read()
    certs = json.loads(certs)

    # will throw error if not valid
    user = jwt.decode(idToken, certs, algorithms='RS256',
                      audience=target_audience)
    return user
