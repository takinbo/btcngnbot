```{% for exchange in exchanges %}
{{ "%-13s - " | format(exchange.name) }}{{ exchange.rate | naira }}
{%- endfor %}
{{ "%-13s - " | format("Avg. Price") }}{{ average_rate | naira }}
```
