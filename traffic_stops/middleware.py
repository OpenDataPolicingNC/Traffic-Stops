import re


STATES = ('nc', 'md')
pattern = re.compile(r"^/(\w{2})/")


class StateMiddleware(object):
    """Set request.state to 'nc' or 'md' based on request.path"""
    def process_request(self, request):
        request.state = None
        match = pattern.match(request.path)
        if match and match.group(1) in STATES:
            request.state = match.group(1)
