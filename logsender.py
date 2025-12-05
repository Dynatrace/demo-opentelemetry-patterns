from opentelemetry import _logs
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
import logging

# Configure the OTLP exporter for gRPC
otlp_exporter = OTLPLogExporter(
    endpoint="localhost:4317",
    insecure=True
)

# Set up the logger provider with resource attributes
resource = Resource.create({"service.name": "logsender"})
logger_provider = LoggerProvider(resource=resource)

# Add the batch processor with the exporter
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(otlp_exporter)
)

# Set the global logger provider
_logs.set_logger_provider(logger_provider)

# Get a logger
logger = _logs.get_logger(__name__)

# Send a log with attributes
log_record = _logs.LogRecord(
        timestamp=None,
        severity_number=_logs.SeverityNumber.INFO,
        severity_text="INFO",
        body="This is a test log message",
        attributes={
            "custom.attribute": "value1",
            "user.id": "12345",
            "environment": "production"
        }
    )
logger.emit(log_record)

# Force flush to ensure logs are sent
logger_provider.force_flush()

print("Log sent successfully!")
