from bottle import Bottle, request
from esql.utility.configure import Environment

# create wsgi app
app = application = Bottle()

# create esql environment
env = Environment()


from esql import parser, generator
from esql.generator import execute

parser.init(env.config['parser'])
generator.init()


@app.route('/es', method=('GET', 'POST'))
def es_sql():
    """ Execute Sql in ES
    """
    request_data = request.forms if request.method == 'POST' else request.query
    sql = request_data.get('sql')
    return execute(sql)
