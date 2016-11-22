from fuzzywuzzy import process
from jinja2 import Environment, FileSystemLoader
from mwt import MWT
import exchanges as ex

env = Environment(loader=FileSystemLoader(['templates']))
exchanges = {klass.symbol: klass for klass in ex.__exchanges__}

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

if __name__ == '__main__':
    pass
