class ParseRequests:
    def __init__(self, environ):
        self.request_data = environ

    def parse_query_string(self, d_str):
        """
            :return: словарь вида {'id': 1, 'category': 5}
        """
        res = {}
        if d_str:
            params = d_str.split('&')
            for item in params:
                key, value = item.split('=')
                res[key] = value
        return res


class ParseGetRequests(ParseRequests):
    def __init__(self, environ):
        super().__init__(environ)
        self.query_string = environ['QUERY_STRING']

    def parse(self):
        self.request_params = super().parse_query_string(self.query_string)
        return self.request_params


class ParsePostRequests(ParseRequests):
    def __init__(self, environ):
        super().__init__(environ)
        self.content_length_data = self.request_data['CONTENT_LENGTH']

    def parse(self):
        self.result = {}
        self.content_length = int(self.content_length_data) if self.content_length_data else 0
        self.data = self.request_data['wsgi.input'].read(self.content_length) if self.content_length > 0 else b''
        if self.data:
            self.data_str = self.data.decode(encoding='utf-8')
            self.result = super().parse_query_string(self.data_str)
        return self.result
