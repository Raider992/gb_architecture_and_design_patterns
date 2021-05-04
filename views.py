from satou_framework.templator import render

class Main:
    def __call__(self, request):
        return '200 OK', render('main.html', data=request.get('data', None))


class Other:
    def __call__(self, request):
        return '200 OK', render('other.html')


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'