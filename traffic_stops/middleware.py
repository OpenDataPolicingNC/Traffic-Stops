import re


STATES = ('nc', 'md', 'il')
pattern = re.compile(r"^/(\w{2})/")


class StateMiddleware(object):
    """Set request.state based on request.path"""
    def process_request(self, request):
        request.state = None
        match = pattern.match(request.path)
        if match and match.group(1) in STATES:
            request.state = match.group(1)
