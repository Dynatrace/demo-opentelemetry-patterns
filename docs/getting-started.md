You will need to collect some information before you can begin.

--8<-- "snippets/bizevent-getting-started.js"

## Prerequisites
- A Dynatrace tenant ([sign up for a free trial](https://dt-url.net/trial){target=_blank})
- A Dynatrace API token with `logs.ingest` permissions (see below)

## Format URL

Make a note of your Dynatrace tenant ID. It is the first bit of your URL (eg. `abc12345` in the following examples):

```
https://abc12345.live.dynatrace.com
https://abc12345.apps.dynatrace.com
```

## Environment Type

Make a note of your environment type. The above environment type is `live`. If in doubt, use `live`.

## Create API Token

In Dynatrace:

* Press `ctrl + k` and search for `access tokens`
* Create a new access token with the `logs.ingest` permission

You have all the necessary details and are ready to get started.

<div class="grid cards" markdown>
- [Click here to continue :octicons-arrow-right-24:](start-demo.md)
</div>
