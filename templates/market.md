```
Exchange        Buy          Sell
{%- for exchange in exchanges %}
{{ "%-13s - " | format(exchange.name) }}{{ "%-13s" | format(exchange.ask | naira) }}{{ exchange.bid | naira }}
{%- endfor -%}
```
