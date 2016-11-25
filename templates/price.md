```{% for exchange in exchanges %}
{{ "%-7s - " | format(exchange.name) }}{{ exchange.rate | naira }}
{%- endfor %}
{{ "%-7s - " | format("Average") }}{{ average_rate | naira }}
```
