# Batching Telemetry

--8<-- "snippets/bizevent-scenario1.js"

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

## Verify Debug Data in Collector Output

View the collector terminal window and verify that the filelog receiver has sent the data to the collector. You should see terminal output like this:

```
...
2025-03-26T06:49:00.944Z        info    Logs    {"kind": "exporter", "data_type": "logs", "name": "debug", "resource logs": 1, "log records": 1}
2025-03-26T06:49:00.944Z        info    ResourceLog #0
Resource SchemaURL: 
ScopeLogs #0
ScopeLogs SchemaURL: 
InstrumentationScope  
LogRecord #0
ObservedTimestamp: 2025-03-26 06:48:59.538241971 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(My first dummy log line...)
Attributes:
     -> log.file.name: Str(file.log)
Trace ID: 
Span ID: 
Flags: 0
        {"kind": "exporter", "data_type": "logs", "name": "debug"}
```

## View Data in Dynatrace

In Dynatrace:

- Press `ctrl + k` and search for `notebooks`
- Create a new notebook and add a new DQL tile with this code:
```
fetch logs
| filter contains(content, "dummy log line")
```

Notice that the batching was entirely transparent to you.

<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](scenario2.yaml)
</div>
