#!/usr/bin/env python3
import os
import subprocess
import click
from google import genai
from google.genai.types import HttpOptions, GenerateContentConfig

# Load API key from environment
API_KEY = "GEMINI_API_KEY"  # Set your environment variable here
if not API_KEY:
    raise RuntimeError("Please set the GEMINI_API_KEY environment variable")

# Instantiate client (Gemini Developer API)
client = genai.Client(api_key=API_KEY, http_options=HttpOptions(api_version="v1alpha"))
MODEL_NAME = "gemini-2.5-flash"  # adjust as needed

import subprocess

def gather_system_context() -> str:
    try:
        # Get installed packages (top 20 for brevity)
        installed_pkgs = subprocess.run("dpkg -l | head -n 25", shell=True, check=True, stdout=subprocess.PIPE, text=True).stdout.strip()
        # Get top files in root directory (top 20 for brevity)
        top_files = subprocess.run("ls -l / | head -n 20", shell=True, check=True, stdout=subprocess.PIPE, text=True).stdout.strip()
        context = f"Installed packages:\n{installed_pkgs}\n\nTop files in root directory:\n{top_files}\n"
        return context
    except Exception as e:
        return f"Could not gather system context: {e}"

SYSTEM_PROMPT = """
You are a Linux terminal assistant. Convert user instruction into safe, single-line bash commands.
Only return the command list, one per line, nothing else. if you cannot determine a command, return an text for users query.
"""

def get_commands(prompt: str) -> list[str]:
    system_context = gather_system_context()
    full_prompt = f"{SYSTEM_PROMPT}\nSystem context:\n{system_context}\nUser: {prompt}"
    resp = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt,
        config=GenerateContentConfig(temperature=0.2)
    )
    text = resp.text
    if text.splitlines() is None:
        # Fallback: attempt to serialize or capture candidates
        fallback = getattr(resp, "candidates", None)
        print("⚠️ resp.text is None; resp object:", resp)
        if fallback:
            print("Candidates:", fallback)
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]

def execute(command: str) -> str:
    try:
        r = subprocess.run(command, shell=True, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return r.stdout.strip() or "<no output>"
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

@click.command()
@click.argument("prompt", nargs=-1, required=True)
def cli(prompt):
    prompt_text = " ".join(prompt)
    cmds = get_commands(prompt_text)
    if not cmds:
        click.echo("⚠️ No parsed commands. Printing raw Gemini response:")
        # Note: get_commands already prints resp or candidates
        return

    click.echo("🔧 Proposed commands:")
    for i, c in enumerate(cmds, 1):
        click.echo(f" {i}. {c}")

    if not click.confirm("Execute these commands?"):
        click.echo("Aborted.")
        return

    click.echo("\n📤 Running commands...\n")
    for c in cmds:
        click.echo(f"$ {c}")
        out = execute(c)
        click.echo(out + "\n")

if __name__ == "__main__":
    cli()
