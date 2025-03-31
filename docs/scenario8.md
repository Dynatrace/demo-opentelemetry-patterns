# Dropping Logs based on Content

--8<-- "snippets/bizevent-scenario8.js"

Up to now, we have been processing and rewriting log content as it flows through the collector.

What if instead, you simply want to drop any logs if they contain restricted content?

In this scenario, to protect against Personally Identifiable Information (PII) capture, the [filter](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/filterprocessor/README.md){target=_blank} processor will be used to drop any log lines containing the word `password` (case insensitive).

[scenario8.yaml](https://github.com/Dynatrace/demo-opentelemetry-cleanup/blob/main/scenario8.yaml){target=_blank} shows the OpenTelemetry collector configuration to achieve this.

## Stop Previous Collector

If you haven't done so already, stop the previous collector process by pressing `Ctrl + C`.

## Start Collector

Run the following command to start the collector:

``` { "name": "[background] run otel collector scenario 8" }
/workspaces/$RepositoryName/dynatrace-otel-collector --config=/workspaces/$RepositoryName/scenario8.yaml
```

!!! tip "Ordering matters"
    Notice the `service.pipelines.logs.processors` definition.
    
    `filter` is defined first so log lines are filtered first before further processing.

    ```
    processors: [filter, resourcedetection, transform, batch]
    ```

## Generate Log Data

Open `file.log` file and add this line then save the file.

```
My eighth dummy log line. The password is abc124
```

## Verify Debug Data in Collector Output

View the collector terminal window and verify that there is absolutely no record of the offending line in the collector logs:


* `user.tier` piece has been rewritten to `userTier`
* `support.tier` attribute has been added due to `userTier` being present in the log content


```
...
Body: Str(My seventh dummy log line from userId=4321 part of userTier=tier3)
Attributes:
     ...
     -> support.tier: Str(bronze)
...
```

## View Data in Dynatrace

As you may expect, there is nothing to see in Dynatrace.

Congratulations! You can now prevent logs from being persisted based on their content.


<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](scenario9.md)
</div>
