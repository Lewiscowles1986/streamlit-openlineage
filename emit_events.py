from datetime import UTC, datetime
import json
import os
import sys
from typing import TYPE_CHECKING
from openlineage.client import OpenLineageClient
from openlineage.client.transport.file import FileTransport, FileConfig
from openlineage.client.event_v2 import (
    RunEvent,
    Run,
    Job,
    RunState,
    InputDataset,
    OutputDataset,
)
import attr
from pathlib import Path
from uuid_extension import uuid7
if TYPE_CHECKING:
    from openlineage.client.client import Event

cwd = Path.cwd()
base_dir_events = f"{cwd}/openlineage_events"
os.makedirs(base_dir_events, exist_ok=True)
client = OpenLineageClient(transport=FileTransport(FileConfig(log_file_path=f"{base_dir_events}/event")))
# path=f"{cwd}/openlineage_events"))
job_id = f"{uuid7()}"
process_id = f"{uuid7()}"
process_instance_id = f"{uuid7()}"
file_id = f"{uuid7()}"
task_extract_content_id = f"{uuid7()}"
task_review_extract_id = f"{uuid7()}"

event = RunEvent(
    eventType=RunState.COMPLETE,
    eventTime="2025-10-22T00:00:00Z",
    run=Run(runId=job_id),
    job=Job(namespace="default", name="upload_documents"),
    producer="https://example.com/my-producer",
    inputs=[InputDataset(namespace="default", name="subscription_document.pdf")],
    outputs=[OutputDataset(namespace="default", name=f"/process/{process_id}/{process_instance_id}/{file_id}")]
)
client.emit(event)

event = RunEvent(
    eventType=RunState.COMPLETE,
    eventTime="2025-10-22T00:01:00Z",
    run=Run(runId=job_id),
    job=Job(namespace="default", name="extract_content"),
    producer="https://example.com/my-producer",
    inputs=[InputDataset(namespace="default", name=f"/process/{process_id}/{process_instance_id}/{file_id}")],
    outputs=[OutputDataset(namespace="default", name=f"postgres://amwb.motive_lewis_automation.tasks.{task_extract_content_id}.result")]
)
client.emit(event)

event = RunEvent(
    eventType=RunState.COMPLETE,
    eventTime="2025-10-22T00:02:00Z",
    run=Run(runId=job_id),
    job=Job(namespace="default", name="review_extract"),
    producer="https://example.com/my-producer",
    inputs=[
        InputDataset(namespace="default", name=f"/process/{process_id}/{process_instance_id}/{file_id}"),
        InputDataset(namespace="default", name=f"postgres://amwb.motive_lewis_automation.tasks.{task_extract_content_id}.result"),
    ],
    outputs=[
        OutputDataset(namespace="default", name=f"postgres://amwb.motive_lewis_automation.tasks.{task_review_extract_id}.result")
    ]
)
client.emit(event)
