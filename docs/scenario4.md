# Setting default severity / status

--8<-- "snippets/bizevent-scenario4.js"

The log lines ingested from the previous scenarious contain no severity information (eg. `DEBUG`, `INFO`, `WARN`, `ERROR` etc).

Setting the correct log severity is important for downstream users to understand how "bad" the log line is - is it simply an informational message or a serious error?

These severities will also be used in later scenarios to (for example) conditionally drop or re-route logs based on their severity.

For now, let's assume that, where a severity is not explicitly set (all of our log lines), we want to default the lines to an `INFO` level log line.

[scenario4.yaml](https://github.com/Dynatrace/demo-opentelemetry-cleanup/blob/main/scenario4.yaml){target=_blank} shows the OpenTelemetry collector configuration to achieve this.

## Look Again

Look again at the collector debug output from scenario 3. You should see that the `SeverityText` and `SeverityNumber` are both empty / unspecified.

```
LogRecord #1
ObservedTimestamp: 2025-03-27 06:04:05.298857978 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText: 
SeverityNumber: Unspecified(0)
Body: Str(My third dummy log line...)
Attributes:
     -> log.file.name: Str(file.log)
     -> log.file.path: Str(/workspaces/demo-opentelemetry-cleanup/file.log)
```

## Stop Previous Collector

If you haven't done so already, stop the previous collector process by pressing `Ctrl + C`.

## Start Collector

Run the following command to start the collector:

``` { "name": "[background] run otel collector scenario 4" }
/workspaces/$RepositoryName/dynatrace-otel-collector --config=/workspaces/$RepositoryName/scenario4.yaml
```

## Generate Log Data

Open `file.log` file and add this line then save the file.

```
My fourth dummy log line...
```

## Verify Debug Data in Collector Output

View the collector terminal window and verify that the `timestamp` and `observed timestamp` fields are now correctly set to the current time and date:

```
...
SeverityText: INFO
SeverityNumber: Info(9)
Body: Str(My fourth dummy log line...)
...
```

## View Data in Dynatrace

--8<-- "snippets/enlarge-image-tip.md"

![scenario4 dynatrace results](images/scenario4-dql.png)

Click the `Run` button again on the DQL tile. You should see the new data.

Reminder, the DQL statement is:

```
fetch logs
| filter contains(content, "dummy log line")
```

Congratulations! The log lines now have the correct timestamps.

<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](scenario5.md)
</div>
