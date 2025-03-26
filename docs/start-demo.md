## Start Demo

--8<-- "snippets/codespace-details-warning-box.md"
--8<-- "snippets/bizevent-start-demo.js"

Click this button to launch the demo in a new tab.

Provide the tenant ID and API token via the form. These will be encrypted and stored in GitHub. They will also automatically be set as environment variables in the codespace.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/dynatrace/demo-opentelemetry-cleanup){target=_blank}

## Understand Demo Environment

The Dynatrace OpenTelemetry Collector (`./dynatrace-otel-collector`) is automatically downloaded at startup. The collector is the syslog server. This collector distribution is officially supported by Dynatrace.

The `filelog` receiver we will soon define (in a YAML file) will watch a log file and send the log lines to the collector.

We will use the collector to process, enrich or drop data.

The collector will then send (export) data into your Dynatrace environment.

The collector requires a configuration file. There are different configuration files for different tasks. Each will be presented as a single "scenario" and explained as you proceed through this guide.

### Understand Collector Configuration

Understanding the configuration of the collector is key to understanding how the data gets from your devices into Dynatrace.

Note: You do not need to modify `scenario*.yaml` files.

#### Receivers

```
receivers:
  ...
```

The receivers block describes how data is received by the collector.

In this case, the [filelog receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/filelogreceiver){target=_blank} is configured to watch log files and ingest them into the collector.

#### Processors

```
processors:
  ...
```

Processors live in the middle of the chain. They process the data in some way before it is sent out to the final destination.

#### Exporters

```
exporters:
  ...
```

The exporters block defines what happens to the data at the point it leaves the collector.

In the following scenarios, 2 exporters are defined: `debug` and `otlphttp`. The `debug` exporter sends output to the collector console. It is included here as a training aid for the demo so you can see what's happening.

The `otlphttp` exporter sends data to an endpoint in OpenTelemetry Protocol (OTLP) format via HTTPS. Dynatrace natively understands the OTLP format.

Notice that two environment variables are referenced: `DT_ENDPOINT` and `DT_API_TOKEN` you may recall these from the form you completed when the codespace started.

These environment variables are already set for you, so you don't need to do anything else.

#### Pipelines

```
service:
  pipelines:
    logs:
      receivers: [filelog]
      processors: [batch]
      exporters: [debug, otlphttp]
```

The pipelines block defines how the collector components are connected in an end-to-end pipeline.

In this case, `1` pipeline (dealing with log data) is defined. This pipeline will receive data using the `filelog` receiver, process the data using the `batch` processor (no guesses for what this does) and export it to **both** the `debug` and `otlphttp` exporters simultaneously.

<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](run-demo.md)
</div>
