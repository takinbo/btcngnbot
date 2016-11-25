```
       Buy          Sell
{%- for exchange in exchanges %}
{{ "%-4s - " | format(exchange.name) }}{{ "%-13s" | format(exchange.ask | naira) }}{{ exchange.bid | naira }}
{%- endfor -%}
```
