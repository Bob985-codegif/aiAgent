import subprocess
import sys
import shlex
import os
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field


mcp = FastMCP()

@mcp.tool(name="run_shell", description="Run a shell command")
def run_shell_command(command:
    Annotated[str, Field(description="shell command will be executed", examples="ls -al")]) -> str:
    
    # Debug logging
    with open("D:\\BaiduNetdiskDownload\\ai_agent_with_langchain\\mcp_debug.log", "a", encoding="utf-8") as f:
        f.write(f"Executing command: {command}\n")

    try:
        shell_command = shlex.split(command)
        if "rm" in shell_command:
            raise Exception("不允许使用rm")

        # Determine encoding
        import locale
        import codecs
        system_encoding = locale.getpreferredencoding()

        # Create subprocess
        env = os.environ.copy()
        env['GIT_TERMINAL_PROMPT'] = '0'  # Fail instead of prompting for password
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirect stderr to stdout
            text=False,  # Binary mode
            bufsize=0,   # Unbuffered
            env=env
        )

        output_bytes = bytearray()
        decoder = codecs.getincrementaldecoder(system_encoding)(errors='replace')
        
        # Try to open Windows Console directly to bypass any stream capturing
        console_file = None
        try:
            if sys.platform == "win32":
                console_file = open('CONOUT$', 'w', encoding=system_encoding, errors='replace', buffering=1)
        except Exception:
            pass

        with open("D:\\BaiduNetdiskDownload\\ai_agent_with_langchain\\mcp_debug.log", "a", encoding="utf-8") as log_f:
            while True:
                # Read small chunks to get real-time output even without newlines
                chunk = process.stdout.read(1024)
                if not chunk:
                    if process.poll() is not None:
                        break
                    continue
                
                output_bytes.extend(chunk)
                
                # Decode and print
                text_chunk = decoder.decode(chunk, final=False)
                if text_chunk:
                    # Print to stderr for user visibility (fallback)
                    print(text_chunk, end="", file=sys.stderr, flush=True)
                    
                    # Print to Console directly (primary fix)
                    if console_file:
                        try:
                            console_file.write(text_chunk)
                            console_file.flush()
                        except Exception:
                            pass
                            
                    # Log to file
                    log_f.write(text_chunk)
                    log_f.flush()

        if console_file:
            console_file.close()

        process.wait()
        
        # Final decode
        final_output = decoder.decode(b"", final=True) # flush decoder
        full_text_output = decoder.decode(output_bytes, final=True)

        with open("D:\\BaiduNetdiskDownload\\ai_agent_with_langchain\\mcp_debug.log", "a", encoding="utf-8") as f:
            f.write(f"\nCommand finished with return code: {process.returncode}\n")
        
        if process.returncode != 0:
            error_msg = f"\nCommand failed with return code {process.returncode}. Please check the output above for details."
            full_text_output += error_msg
            with open("D:\\BaiduNetdiskDownload\\ai_agent_with_langchain\\mcp_debug.log", "a", encoding="utf-8") as f:
                 f.write(error_msg + "\n")

        return full_text_output
    except Exception as e:
        with open("D:\\BaiduNetdiskDownload\\ai_agent_with_langchain\\mcp_debug.log", "a", encoding="utf-8") as f:
            f.write(f"Error: {str(e)}\n")
        return str(e)



def run_shell_command_by_popen(commands):
    p = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    stdout, stderr = p.communicate()
    if stdout:
        return stdout
    return stderr


if __name__ == "__main__":
    mcp.run(transport="stdio")