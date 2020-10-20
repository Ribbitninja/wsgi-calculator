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

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    total = sum(map(int, args))
    return "<h1>{}</h1>".format(total)


def subtract(*args):
    """ Returns a STRING with the sum of the arguments """
    arg_num = 2
    difference = int(args[0]) - int(args[1])
    while True:
        try:
            difference -= int(args[arg_num])
            arg_num += 1
        except IndexError:
            return "<h1>{}</h1>".format(difference)


def multiply(*args):
    product = 1
    for x in args:
        product *= int(x)
    return "<h1>{}</h1>".format(product)


def divide(*args):
    arg_num = 2
    quotient = int(args[0]) / int(args[1])
    while True:
        try:
            quotient /= int(args[arg_num])
            arg_num += 1
        except IndexError:
            return "<h1>{}</h1>".format(quotient)


# TODO: Add functions for handling more arithmetic operations.


def info():
    body = """<html>
<head>
<title>Lab 3 - WSGI experiments</title>
</head>
<body>
<p>Hello.  This page is a calculator with add, subtract, multiple, and divide functionality.</p>
<p>To perform any of the above operations, enter the operation followed by the arguments.</p>
<p>e.g. "/add/4/2" will return a value of 6.</p>
</body>
</html>"""
    return body


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        "": info,
        'add': add,
        'subtract': subtract,
        'divide': divide,
        'multiply': multiply
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # works here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    import pprint
    pprint.pprint(environ)
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
    pass
