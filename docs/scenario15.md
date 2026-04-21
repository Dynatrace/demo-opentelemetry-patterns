# Filter Log Records from a File

--8<-- "snippets/bizevent-scenario15.js"

Imagine a casino game platform writing security alert events to a log file. Each record captures things like the customer name, bet amounts, cheat detection results, and fraud risk levels. The file contains events for many customers, but you only want to forward records belonging to a specific customer — `Bob Smith` — to your observability backend.

```
{"timestamp":"2026-01-13T12:42:39.176Z","CustomerName":"Sam Smith","cheatType":"lucky_streak","winAmount":0,"Balance":5728,"DetectionRisk":"HIGH","level":"SECURITY_ALERT","event_type":"CASINO_GAME_ACTIVITY","game":"blackjack","category":"FRAUD_DETECTION"}
{"timestamp":"2026-01-13T12:42:39.176Z","CustomerName":"Bob Smith","cheatType":"lucky_streak","winAmount":0,"Balance":5728,"DetectionRisk":"HIGH","level":"SECURITY_ALERT","event_type":"CASINO_GAME_ACTIVITY","game":"blackjack","category":"FRAUD_DETECTION"}
```

[scenario15.yaml](https://github.com/Dynatrace/demo-opentelemetry-patterns/blob/main/scenario15.yaml){target=_blank} shows the base OpenTelemetry collector configuration we'll use during this exercise.

## Step 1: Treat data as JSON Line Format
We (humans) know the data is single line JSON (aka JSONL), but the collector doesn't.

This code tells the collector to expect JSONL formatted data.

```
operators:
  - type: json_parser
```

This automatically transforms the log line into a set of attributes, ready for the next step.

```
Body: Str({"timestamp":"2026-01-13T12:42:39.176Z","CustomerName":"Bob Smith","cheatType":"lucky_streak","winAmount":0,"Balance":5728,"CorrelationId":"743c9bf9517c7211","DetectionRisk":"HIGH","requires_investigation":true,"BetAmount":25,"multiplier":0,"result":"cards dealt","level":"SECURITY_ALERT","event_type":"CASINO_GAME_ACTIVITY","game":"blackjack","action":"deal","email":"sam.smith@example.com","company_name":"ACME Corp","persona":"IT Manager","booth":"Healthcare Demo","balance_before":5753,"balance_after":5728,"cheat_active":true,"cheat_type":"lucky_streak","cheat_win_boost_applied":false,"cheat_original_win":0,"cheat_boosted_win":0,"correlation_id":"55cb6b222d89caad","user_agent":"Vegas-Casino-Browser","ip_address":"internal","opt_in":true,"severity":"HIGH","category":"FRAUD_DETECTION"})
Attributes:
     -> timestamp: Str(2026-01-13T12:42:39.176Z)
     -> cheat_active: Bool(true)
     -> winAmount: Double(0)
     -> level: Str(SECURITY_ALERT)
     -> CorrelationId: Str(743c9bf9517c7211)
     -> balance_before: Double(5753)
     -> cheat_type: Str(lucky_streak)
     -> cheatType: Str(lucky_streak)
     -> cheat_original_win: Double(0)
     -> cheat_boosted_win: Double(0)
     -> category: Str(FRAUD_DETECTION)
     -> severity: Str(HIGH)
     -> ip_address: Str(internal)
     -> BetAmount: Double(25)
     -> company_name: Str(ACME Corp)
     -> persona: Str(IT Manager)
     -> game: Str(blackjack)
     -> event_type: Str(CASINO_GAME_ACTIVITY)
     -> email: Str(sam.smith@example.com)
     -> Balance: Double(5728)
     -> DetectionRisk: Str(HIGH)
     -> multiplier: Double(0)
     -> result: Str(cards dealt)
     -> booth: Str(Healthcare Demo)
     -> balance_after: Double(5728)
     -> correlation_id: Str(55cb6b222d89caad)
     -> action: Str(deal)
     -> opt_in: Bool(true)
     -> CustomerName: Str(Bob Smith)
     -> log.file.name: Str(scenario15.jsonl)
     -> requires_investigation: Bool(true)
     -> cheat_win_boost_applied: Bool(false)
     -> user_agent: Str(Vegas-Casino-Browser)
```

## Step 2: Filter out records

This part is easy. The `filter` processor is used to filter **out** any log records where the `CustomerName` attribute does **not** equal `Bob Smith`.

```
filter:
    error_mode: ignore
    logs:
      log_record:
        - 'attributes["CustomerName"] != "Bob Sm1ith"'
```

## Tie it all together

Always remember to actually use your configuration by adding it to a pipeline otherwise you won't see what you expect!

```
service:
  pipelines:
    logs:
      receivers: [filelog]
      processors: [filter]
      exporters: [debug]
```
### Stop Previous Collector

If you haven't done so already, stop the previous collector process by pressing `Ctrl + C`.

### Start Collector

Run the following command to start the collector:

``` { "name": "[background] run otel collector scenario 15" }
source .env
$BASE_DIR/dynatrace-otel-collector --config=$BASE_DIR/scenario15.yaml
```

### Validate Data in Collector Output

Switch terminals back to the collector and you should see output like this.

Notice how only the `Bob Smith` record appears — the `Sam Smith` record has been filtered out.

```
2026-01-13T12:42:39.176+1000    info    Logs    {"resource logs": 1, "log records": 1}
2026-01-13T12:42:39.176+1000    info    ResourceLog #0
Resource SchemaURL:
Resource attributes:
ScopeLogs #0
ScopeLogs SchemaURL:
InstrumentationScope
LogRecord #0
ObservedTimestamp: 2026-01-13 02:42:39.176 +0000 UTC
Timestamp: 1970-01-01 00:00:00 +0000 UTC
SeverityText:
SeverityNumber: Unspecified(0)
Body: Str({"timestamp":"2026-01-13T12:42:39.176Z","CustomerName":"Bob Smith",...})
Attributes:
     -> CustomerName: Str(Bob Smith)
     -> cheatType: Str(lucky_streak)
     -> winAmount: Int(0)
     -> Balance: Int(5728)
     -> DetectionRisk: Str(HIGH)
     -> level: Str(SECURITY_ALERT)
     -> event_type: Str(CASINO_GAME_ACTIVITY)
     -> game: Str(blackjack)
     -> category: Str(FRAUD_DETECTION)
     -> log.file.name: Str(scenario15.jsonl)
     -> log.file.path: Str(scenario15.jsonl)
Trace ID:
Span ID:
Flags: 0
```

## Explanation

The `filelog` receiver watches `scenario15.jsonl` and reads it from the beginning each time the collector starts.

The `json_parser` operator parses each line as a JSON object and promotes all top-level fields to log record attributes — so `CustomerName`, `DetectionRisk`, `game`, and so on all become queryable attributes.

The `filter` processor then drops any log record where `attributes["CustomerName"] != "Bob Smith"`. Because the filter condition describes what to **drop**, all records that are *not* Bob Smith are discarded, and only his records pass through to the exporter.

This is a common pattern when you have a shared log file produced by a multi-tenant system and you want to route or forward only a specific subset of events.

For more filtering options, see the [filter processor documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/filtprocessor){target=_blank}.

<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](scenario16.md)
</div>
