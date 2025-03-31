# Dynamically Re-writing log lines for standardisation

--8<-- "snippets/bizevent-scenario7.js"

Imagine a new starter joins the development team.

They are informed of the team standards - that logs with `userTier=...` are required to make the Observability system work.

However, they forget and so write their logs with `user.tier=...` instead.

!!! question
    Can the OpenTelemetry collector fix this?

Yes! The transform processor can be used to rewrite the log line in real time so `user.tier` becomes `userTier` with this statement:

```
replace_pattern(body, "user.tier=", "userTier=")
```

[scenario7.yaml](https://github.com/Dynatrace/demo-opentelemetry-cleanup/blob/main/scenario7.yaml){target=_blank} shows the OpenTelemetry collector configuration to achieve this.

## Stop Previous Collector

If you haven't done so already, stop the previous collector process by pressing `Ctrl + C`.

## Start Collector

Run the following command to start the collector:

``` { "name": "[background] run otel collector scenario 7" }
/workspaces/$RepositoryName/dynatrace-otel-collector --config=/workspaces/$RepositoryName/scenario7.yaml
```

## Generate Log Data

Open `file.log` file and add this line then save the file.

```
My seventh dummy log line from userId=4321 part of user.tier=tier3
```

## Verify Debug Data in Collector Output

View the collector terminal window and verify two things:


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

--8<-- "snippets/enlarge-image-tip.md"

![scenario5 dynatrace results](images/scenario7-dql.png)

There are a lot of columns shown so either scroll all the way to the right to see the `support.tier` column.

Or cleanup the columns by choosing to keep only certain columns:

```
fetch logs
| filter contains(content, "dummy log line")
| fieldsKeep timestamp, content, host.name, log.file.name, log.file.path, os.type, support.tier
```

Click the `Run` button again on the DQL tile. You should see the new data.

Congratulations! You can now add any important Key/Value information as logs flow through the collector.

<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](scenario8.md)
</div>
