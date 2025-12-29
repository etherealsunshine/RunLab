"""
Modal.com integration for running containers with compute resources
Handles job execution, output mounting, and status tracking
"""
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
import os

from ..models.schemas import RunmeSpec, JobStatus


class ModalRunner:
    """
    Orchestrates container execution on Modal.com

    In development mode, this simulates execution.
    In production, it will actually deploy to Modal.
    """

    def __init__(self, mock_mode: bool = True):
        """
        Initialize the Modal runner

        Args:
            mock_mode: If True, simulates execution instead of actually running on Modal
        """
        self.mock_mode = mock_mode
        self.jobs: Dict[str, JobStatus] = {}

    def run_job(
        self,
        spec: RunmeSpec,
        command: str,
        inputs: Dict[str, Any]
    ) -> JobStatus:
        """
        Execute a job on Modal.com

        Args:
            spec: The parsed RunmeSpec
            command: The built command to execute
            inputs: The validated user inputs

        Returns:
            JobStatus object with job information
        """
        job_id = str(uuid.uuid4())

        if self.mock_mode:
            return self._mock_execution(job_id, spec, command, inputs)
        else:
            return self._real_execution(job_id, spec, command, inputs)

    def _mock_execution(
        self,
        job_id: str,
        spec: RunmeSpec,
        command: str,
        inputs: Dict[str, Any]
    ) -> JobStatus:
        """Simulate job execution for development"""
        job = JobStatus(
            job_id=job_id,
            status="completed",
            created_at=datetime.utcnow().isoformat(),
            completed_at=datetime.utcnow().isoformat(),
            logs=f"[MOCK MODE] Would execute:\n{command}\n\nWith inputs: {inputs}",
            output_urls=["https://example.com/mock-output.txt"] if spec.outputs.mount_to_s3 else None
        )

        self.jobs[job_id] = job
        return job

    def _real_execution(
        self,
        job_id: str,
        spec: RunmeSpec,
        command: str,
        inputs: Dict[str, Any]
    ) -> JobStatus:
        """
        Actually execute on Modal.com

        This creates a Modal function dynamically based on the spec
        """
        try:
            import modal

            # Create Modal app
            stub = modal.Stub(f"runlab-{spec.name}")

            # Parse GPU requirement
            gpu_config = None
            if spec.compute.gpu and spec.compute.gpu.lower() != "none":
                gpu_config = spec.compute.gpu

            # Parse memory requirement (e.g., "8GB" -> 8192)
            memory_mb = self._parse_memory(spec.compute.memory)

            # Create the function
            @stub.function(
                image=modal.Image.from_registry(spec.container.image),
                cpu=spec.compute.cpu,
                memory=memory_mb,
                gpu=gpu_config,
                timeout=spec.compute.timeout,
            )
            def run_container():
                import subprocess
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=spec.container.working_dir
                )
                return {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }

            # Execute the function
            with stub.run():
                result = run_container.remote()

            # Create job status
            job = JobStatus(
                job_id=job_id,
                status="completed" if result["returncode"] == 0 else "failed",
                created_at=datetime.utcnow().isoformat(),
                completed_at=datetime.utcnow().isoformat(),
                logs=f"STDOUT:\n{result['stdout']}\n\nSTDERR:\n{result['stderr']}",
                error=result['stderr'] if result['returncode'] != 0 else None,
                output_urls=None  # TODO: Implement S3 upload
            )

            self.jobs[job_id] = job
            return job

        except Exception as e:
            job = JobStatus(
                job_id=job_id,
                status="failed",
                created_at=datetime.utcnow().isoformat(),
                completed_at=datetime.utcnow().isoformat(),
                error=str(e),
                logs=f"Error during execution: {str(e)}"
            )
            self.jobs[job_id] = job
            return job

    def get_job_status(self, job_id: str) -> Optional[JobStatus]:
        """Get the status of a job by ID"""
        return self.jobs.get(job_id)

    def _parse_memory(self, memory_str: str) -> int:
        """
        Parse memory string to MB

        Examples:
            "8GB" -> 8192
            "4096MB" -> 4096
            "1G" -> 1024
        """
        memory_str = memory_str.upper().strip()

        if "GB" in memory_str or "G" in memory_str:
            num = float(memory_str.replace("GB", "").replace("G", "").strip())
            return int(num * 1024)
        elif "MB" in memory_str or "M" in memory_str:
            num = float(memory_str.replace("MB", "").replace("M", "").strip())
            return int(num)
        else:
            # Assume MB if no unit
            return int(memory_str)
