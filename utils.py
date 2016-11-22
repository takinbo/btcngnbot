from fuzzywuzzy import process
from jinja2 import Environment, FileSystemLoader
from mwt import MWT
import exchanges as ex

exchanges = {klass.symbol: klass for klass in ex.__exchanges__}

def naira(value):
    if value:
        return "₦{:,.2f}".format(float(value))
    else:
        return "???"

def btc(value):
    if value:
        return "฿{:.8g}".format(float(value))
    else:
        return "???"

env = Environment(loader=FileSystemLoader(['templates']))
env.filters['naira'] = naira
env.filters['btc'] = btc

def render_to_string(template_name, context={}):
    return env.get_template(template_name).render(**context)

def make_choice(selection, options):
    choice = process.extractOne(selection, options, score_cutoff=60)
    if choice:
        return choice[0]

@MWT(timeout=10)
def get_exchange_rate(exchange=None):
    if exchange:
        klass = exchanges[exchange]
        return klass().exchange_rate()
    else:
        rates = [get_exchange_rate(e) for e in exchanges.keys()]
        return sum(rates)/len(rates)

@MWT(timeout=10)
def get_exchange_ticker(exchange):
    klass = exchanges[exchange]
    return klass().ticker()

if __name__ == '__main__':
    pass
