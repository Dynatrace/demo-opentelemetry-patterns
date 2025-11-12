# Parse CSV Files

--8<-- "snippets/bizevent-scenario12.js"

!!! tip "CSV Enrichment"
    This page describes how to send a CSV file into Dynatrace for logging purposes.
    If instead you want to USE a CSV to enrich logs (ie. take a log and dynamically add CSV fields) then you're looking for the functionality provided by [Dynatrace lookup tables](https://www.youtube.com/watch?v=-I6QPwylOfQ&t=401s){target=_blank}

    <iframe width="560" height="315" src="https://www.youtube.com/embed/-I6QPwylOfQ?si=aGLOfQhsZPy2veXl&amp;start=400" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


Imagine you have a CSV file that represents an ever growing list of forums posts: the date it was first posted, who asked the question and who answered it into Dynatrace. How do you do get this data into Dynatrace?

```
Post,Asked By,Answered,Date Posted
https://example.com/post/1,Anna,Bob,21/11/2025
https://example.com/post/2,Bob,Sarah,22/11/2025
https://example.com/post/3,Ian,Kris,22/11/2025
```

[scenario12.yaml](https://github.com/Dynatrace/demo-opentelemetry-patterns/blob/main/scenario12.yaml){target=_blank} shows the base OpenTelemetry collector configuration we'll use during this exercise.

### Stop Previous Collector

If you haven't done so already, stop the previous collector process by pressing `Ctrl + C`.

### Start Collector

Run the following command to start the collector:

``` { "name": "[background] run otel collector scenario 11" }
source /workspaces/$RepositoryName/.env
/workspaces/$RepositoryName/dynatrace-otel-collector --config=/workspaces/$RepositoryName/scenario12.yaml
```

### Generate DataLog Data

Open the `example.csv` file and add these lines then save the file.

```
Post,Asked By,Answered,Date Posted
https://example.com/post/1,Anna,Bob,21/11/2025
https://example.com/post/2,Bob,Sarah,22/11/2025
https://example.com/post/3,Ian,Kris,22/11/2025
```

### View Data in Dynatrace

--8<-- "snippets/enlarge-image-tip.md"

![scenario12 dynatrace results](images/scenario12-dql-1.png)

Open a new notebook (or add a DQL section to an existing notebook).

```
fetch logs
| search "https://example.com/post"
| fieldsKeep timestamp, content, `post`, `asked by`, `answered`, `date posted`
```

Click the `Run` button on the DQL tile. You should see the new data.

## Explanation

The filelog receiver of the collector is configured to watch for changes to `example.csv`.

When new content is detected, the filelog receiver ingests that data and parses it using the [csv_parser operator](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/pkg/stanza/docs/operators/csv_parser.md){target=_blank}.

We have informed the csv_parser that it should expect a header row with the named fields - if it doesn't find one, it will dynamically add those fields to the log records - meaning you can also send in CSV content without a header row.

Finally we've told the csv_parser that a comma will be the field delimiter.

The end result is a log record that looks like this as it flows through the collector (notice the data has been transformed to dedicated attributes):

```
LogRecord #0
ObservedTimestamp: 2025-11-12 05:29:26.4341502 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str(https://example.com/post/1,Anna,Bob,21/11/2025)
Attributes:
     -> Asked By: Str(Anna)
     -> Answered: Str(Bob)
     -> Date Posted: Str(21/11/2025)
     -> log.file.name: Str(example.csv)
     -> log.file.path: Str(example.csv)
     -> Post: Str(https://example.com/post/1)
Trace ID:
Span ID:
Flags: 0
```