# Scenario 1: Batching Telemetry

--8<-- "snippets/bizevent-run-demo.js"

In order to reduce load on both the collector and Dynatrace, you most likely do **not** want to send every log line individually.

Rather, the log lines should be bundled and sent to Dynatrace in batches.

[scenario1.yaml](../scenario1.yaml) shows the OpenTelemetry collector configuration to achieve this.

## Start Collector

Run the following command to start the collector:

``` { "name": "[background] run otel collector scenario 1" }
/workspaces/$RepositoryName/dynatrace-otel-collector --config=/workspaces/$RepositoryName/scenario1.yaml
```

## Generate Log Data

Open the empty `file.log` file and add this line then save the file.

```
My first log line...
```

<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](view-data.md)
</div>
