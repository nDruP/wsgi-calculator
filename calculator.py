"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    additives = sum(args)

    return str(additives)

def sub(*args):
    """ Returns a STRING with the difference of the arguments """
    diff = args[0]
    for x in args[1:]:
        diff -= x

    return str(diff)

def mult(*args):
    """ Returns a STRING with the product of the arguments """

    product = args[0]
    for x in args[1:]:
        product = product*x

    return str(product)

def div(*args):
    """ Returns a STRING with the quotient of the arguments """

    quotient = args[0]
    for x in args[1:]:
        quotient = quotient/x

    return str(quotient)


def home():
    """ Returns a STRING for the calculator's home page"""
    ex_urls = [("/multiply/3/5", '15'),
               ("/add/23/42", '65'),
               ("/subtract/23/42", '-19'),
               ("/divide/22/11", '2'),               
    ]
    body = "<h1>Single Operation Calculator</h1>\n"
    body += "<h3>How to use this page: </h3>\n"
    body += "http://localhost:8080/FUNCTION/NUM1/NUM2/...\n"
    body += "<h3>Examples</h3>\n"
    body += "<ul>\n"
    for url, answ in ex_urls:
        body += "<li><a href="+url+'>'
        body += "http://localhost:8080"+url+'</a> => '+answ+'</li>\n'
    body += "</ul>"
    return body

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    functions = {
        '': home,
        'add': add,
        'subtract': sub,
        'multiply': mult,
        'divide': div,
    }
    
    path = path.strip('/').split('/')

    try:
        func = functions[path[0]]
        args = [float(x) for x in path[1:]]
    except (KeyError, ValueError):
        raise NameError

    return func, args

def application(environ, start_response):

    headers = [("Content-type", "text/html")]
    body = "<a href=/>Home</a>"
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body += "<h1>" + func(*args) + "</h1>"
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body += "<h1>Invalid Input</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body += "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
