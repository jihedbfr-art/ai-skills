---
format: "v2"
name: "ffmpeg-video-generation-mcp"
title: "Ffmpeg Video Generation Mcp"
title_fr: "Ffmpeg Video Generation Mcp"
description: "Architectural pattern for building an MCP server that delegates multimedia tasks to FFmpeg for programmatic video and audio generation."
description_fr: "Skill d'ingénierie et de sécurité pour ffmpeg video generation mcp."
domain: "14-multimedia-and-generation"
tags: [cybersecurity, engineering, best-practices]
maturity: "stable"
audience: ["backend-engineer", "security-engineer", "coding-agent"]
requires: ["bash", "git"]
updated: "2026-08-08"
---



## Prerequisites
- Target system, dependencies and environment configured.

## Usage
### Architectural Purpose
Large Language Models cannot natively output video or complex audio streams. By wrapping FFmpeg inside an MCP server, agents can programmatically assemble videos, overlay text, extract audio, and generate slideshows by emitting structured FFmpeg commands.

---

### 1. Core Pattern / Implementation

Provide the AI agent with specific tools to execute constrained FFmpeg commands rather than giving it arbitrary shell access.

```python
@mcp_server.tool()
async def create_slideshow_video(image_dir: str, output_path: str, fps: int = 1) -> str:
    """Create a video slideshow from a directory of images using FFmpeg."""
    command = [
        "ffmpeg",
        "-framerate", str(fps),
        "-pattern_type", "glob",
        "-i", f"{image_dir}/*.jpg",
        "-c:v", "libx264",
        "-r", "30",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    
    process = await asyncio.create_subprocess_exec(
        *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    
    if process.returncode != 0:
        return f"FFmpeg failed: {stderr.decode()}"
    return f"Video successfully created at {output_path}"
```

---

### 2. Cost, Latency & Trade-offs
- **Token Math**: Minimal LLM token cost. The heavy lifting is offloaded to the CPU/GPU.
- **Latency Penalty**: Video encoding is blocking and extremely CPU-intensive. Short clips can take seconds, long clips minutes. The MCP server must handle asynchronous task execution and return a job ID rather than blocking the LLM HTTP request.
- **Trade-off**: Requires FFmpeg installed on the host machine. Security risk if `image_dir` or `output_path` are not sanitized (Path Traversal vulnerabilities).

---

### 3. Verification Checklist
- [ ] File paths are strictly sanitized to prevent directory traversal outside a designated `scratch/` folder.
- [ ] Long-running FFmpeg processes are executed asynchronously, returning a Job ID for polling.
- [ ] CPU limits or queues are implemented to prevent the host server from crashing under multiple concurrent video generation requests.

## Inputs
- Relevant source code, logs, network traces, or system specifications.

## Outputs
- Analysis findings, security audit report, or generated code artifacts.