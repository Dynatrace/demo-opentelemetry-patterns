import os
from utils import *

CODESPACE_NAME = os.environ.get("CODESPACE_NAME", "")
#GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "")

# Download Collector
COLLECTOR_VERSION="0.23.0"
collector_download = build_collector_download_url(COLLECTOR_VERSION)
collector_filename = collector_download["filename"]
run_command(["wget", collector_download["url"]])
if collector_filename.endswith(".zip"):
    run_command(["unzip", "-o", collector_filename])
else:
    run_command(["tar", "-xf", collector_filename])
run_command(["rm", collector_filename])

# Download OpenTelemetry Collector Contrib
OTELCOL_CONTRIB_VERSION="0.150.1"
otelcol_contrib_download = build_otelcol_contrib_download_url(OTELCOL_CONTRIB_VERSION)
otelcol_contrib_filename = otelcol_contrib_download["filename"]
run_command(["wget", otelcol_contrib_download["url"]])
if otelcol_contrib_filename.endswith(".zip"):
    run_command(["unzip", "-o", otelcol_contrib_filename])
else:
    run_command(["tar", "-xf", otelcol_contrib_filename])
run_command(["rm", otelcol_contrib_filename])

# Install RunMe
# if CODESPACE_NAME.startswith("dttest-"):
#     RUNME_CLI_VERSION = "3.10.2"
#     run_command(["mkdir", "runme_binary"])
#     run_command(["wget", "-O", "runme_binary/runme_linux_x86_64.tar.gz", f"https://download.stateful.com/runme/{RUNME_CLI_VERSION}/runme_linux_x86_64.tar.gz"])
#     run_command(["tar", "-xvf", "runme_binary/runme_linux_x86_64.tar.gz", "--directory", "runme_binary"])
#     run_command(["sudo", "mv", "runme_binary/runme", "/usr/local/bin"])
#     run_command(["rm", "-rf", "runme_binary"])

# utils.py creates the .env entries dynamically
# so reload them here and now
load_dotenv()
DT_URL = os.environ.get("DT_URL", "")
# Do placeholder replacements

do_file_replace(pattern=f"/workspaces/{REPOSITORY_NAME}/*.yaml", find_string="DT_ENDPOINT_PLACEHOLDER", replace_string=DT_URL, recursive=False)

if CODESPACE_NAME.startswith("dttest-"):
    run_command(["pip", "install", "-r", f"/workspaces/{REPOSITORY_NAME}/.devcontainer/testing/requirements.txt", "--break-system-packages"])
    run_command(["python",  f"/workspaces/{REPOSITORY_NAME}/.devcontainer/testing/testharness.py"])

    # Testing finished. Destroy the codespace
    run_command(["gh", "codespace", "delete", "--codespace", CODESPACE_NAME, "--force"])
else:
    logger.info("Startup successful...")
    # TODO: Re-enable before push
    #send_startup_ping(demo_name="demo-opentelemetry-patterns")
