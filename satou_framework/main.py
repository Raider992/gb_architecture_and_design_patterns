import quopri
from utils.requests import ParseGetRequests, ParsePostRequests

from views import NotFound404


class Framework:
    def __init__(self, routes_lst, fronts_lst):
        self.routes_list = routes_lst
        self.fronts_list = fronts_lst

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = ParsePostRequests(environ).parse()
            print(type(data))
            request['data'] = data
            print(f'Получен post-запрос: {Framework.decode_value(data)}')

        if method == 'GET':
            request_params = ParseGetRequests(environ).parse()
            request['request_params'] = request_params
            print(f'Получен GET-запрос с параметрами: { request_params }')

        if path in self.routes_list:
            view = self.routes_list[path]
        else:
            view = NotFound404()

        request = {}

        for front in self.fronts_list:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
