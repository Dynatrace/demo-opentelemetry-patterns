# Scenario 1: Batching Telemetry

--8<-- "snippets/bizevent-run-demo.js"

In order to reduce load on both the collector and Dynatrace, you most likely do **not** want to send every log line individually.

Rather, the log lines should be bundled and sent to Dynatrace in batches.

[scenario1.yaml](https://github.com/Dynatrace/demo-opentelemetry-cleanup/blob/main/scenario1.yaml){target=_blank} shows the OpenTelemetry collector configuration to achieve this.

We will first generate the data then explain the YAML configuration.

## Start Collector

Run the following command to start the collector:

``` { "name": "[background] run otel collector scenario 1" }
/workspaces/$RepositoryName/dynatrace-otel-collector --config=/workspaces/$RepositoryName/scenario1.yaml
```

## Generate Log Data

Open the empty `file.log` file and add this line then save the file.

```
My first dummy log line...
```

## View Data in Dynatrace

In Dynatrace:

- Press `ctrl + k` and search for `notebooks`
- Create a new notebook and add a new DQL tile with this code:
```
fetch logs
| filter contains(body, "dummy log line")
```

<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](view-data.md)
</div>
