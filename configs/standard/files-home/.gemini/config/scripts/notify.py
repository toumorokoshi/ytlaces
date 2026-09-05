#!/usr/bin/env python3
import json
import os
import re
import shutil
import subprocess
import sys

def escape_applescript(text: str) -> str:
    """Escapes string for inclusion in an AppleScript double-quoted literal."""
    if not text:
        return ""
    cleaned = " ".join(text.split())
    return cleaned.replace("\\", "\\\\").replace('"', '\\"')

def send_notification(title: str, subtitle: str, message: str, sound: str = "Glass"):
    """Dispatches a desktop notification on macOS or Linux."""
    if sys.platform == "darwin":
        t = escape_applescript(title)
        s = escape_applescript(subtitle)
        m = escape_applescript(message)
        snd = escape_applescript(sound)
        script = f'display notification "{m}" with title "{t}" subtitle "{s}" sound name "{snd}"'
        try:
            subprocess.run(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except Exception:
            pass
    elif sys.platform.startswith("linux"):
        summary = f"{title}: {subtitle}" if subtitle else title
        try:
            if shutil.which("notify-send"):
                urgency = "critical" if sound in ["Basso", "Ping"] else "normal"
                subprocess.run(["notify-send", "-a", title, "-u", urgency, summary, message], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except Exception:
            pass

def extract_latest_model_question(transcript_path: str):
    """
    Checks if the latest model response contains a question or requests user input.
    Returns (is_question, question_text).
    """
    if not transcript_path or not os.path.exists(transcript_path):
        return False, ""
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines):
            try:
                data = json.loads(line)
                if data.get("type") == "PLANNER_RESPONSE" and data.get("content"):
                    content = data["content"].strip()
                    cleaned = re.sub(r"```[\s\S]*?```", "", content)
                    cleaned = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", cleaned)
                    lines_clean = [l.strip() for l in cleaned.splitlines() if l.strip()]
                    if not lines_clean:
                        return False, ""
                    
                    check_tail = " ".join(lines_clean[-3:])
                    
                    q_match = re.findall(r"([^.?!\n]{5,}\?)", check_tail)
                    if q_match:
                        q_text = " ".join(q_match[-1].strip().split())
                        q_text = re.sub(r"[*_`#>-]", "", q_text).strip()
                        if len(q_text) > 90:
                            q_text = q_text[:87] + "..."
                        return True, q_text
                    
                    lower_tail = check_tail.lower()
                    prompt_triggers = ["let me know", "would you like", "should i", "do you want", "please choose", "please select"]
                    for trigger in prompt_triggers:
                        if trigger in lower_tail:
                            last_line = re.sub(r"[*_`#>-]", "", lines_clean[-1]).strip()
                            if len(last_line) > 90:
                                last_line = last_line[:87] + "..."
                            return True, last_line
                    
                    return False, ""
            except Exception:
                continue
    except Exception:
        pass
    return False, ""

def get_last_user_prompt(transcript_path: str) -> str:
    """Extracts the latest user prompt from the conversation transcript."""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""
    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in reversed(lines):
            try:
                data = json.loads(line)
                if data.get("type") == "USER_INPUT":
                    content = data.get("content", "")
                    m = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                    if m:
                        content = m.group(1)
                    content = re.sub(r"<[^>]+>", "", content)
                    cleaned = " ".join(content.strip().split())
                    if len(cleaned) > 90:
                        return cleaned[:87] + "..."
                    return cleaned
            except Exception:
                continue
    except Exception:
        pass
    return ""

def main():
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception:
        payload = {}

    tool_call = payload.get("toolCall")
    workspace_paths = payload.get("workspacePaths", [])
    workspace_name = os.path.basename(workspace_paths[0]) if workspace_paths and workspace_paths[0] else "Antigravity"

    # Case 1: PreToolUse (Tool execution / Approval Needed)
    if tool_call:
        tool_name = tool_call.get("name", "")
        args = tool_call.get("args", {})
        
        is_approval = (
            args.get("BypassSandbox") is True 
            or str(args.get("BypassSandbox")).lower() == "true"
            or args.get("requiresApproval") is True
        )
        
        if is_approval:
            cmd = args.get("CommandLine") or args.get("toolAction") or tool_name
            msg = f"Allow: {cmd}"
            if len(msg) > 90:
                msg = msg[:87] + "..."
            
            send_notification(
                title="Antigravity",
                subtitle=f"{workspace_name} • Approval Needed",
                message=msg,
                sound="Ping"
            )
            print(json.dumps({"decision": "ask", "reason": "Requires user approval"}))
            return

        if tool_name == "ask_question":
            questions = args.get("questions", [])
            q_text = "The agent is asking a question."
            if questions and isinstance(questions, list) and "question" in questions[0]:
                q_text = questions[0]["question"]
            
            send_notification(
                title="Antigravity",
                subtitle=f"{workspace_name} • Input Needed",
                message=q_text,
                sound="Ping"
            )
            print(json.dumps({"decision": "allow"}))
            return
            
        # Allow ordinary tool calls silently
        print(json.dumps({"decision": "allow"}))
        return

    # Case 2: Stop (Turn completion / model finished response)
    transcript_path = payload.get("transcriptPath", "")
    error_msg = payload.get("error")
    
    if error_msg:
        send_notification(
            title="Antigravity",
            subtitle=f"{workspace_name} • Task Failed",
            message=error_msg,
            sound="Basso"
        )
    else:
        is_question, q_snippet = extract_latest_model_question(transcript_path)
        
        if is_question and q_snippet:
            send_notification(
                title="Antigravity",
                subtitle=f"{workspace_name} • Input Needed",
                message=q_snippet,
                sound="Ping"
            )
        else:
            prompt_summary = get_last_user_prompt(transcript_path)
            if not prompt_summary:
                prompt_summary = "Task completed successfully."
            
            send_notification(
                title="Antigravity",
                subtitle=f"{workspace_name} • Task Completed",
                message=prompt_summary,
                sound="Glass"
            )

    print(json.dumps({}))

if __name__ == "__main__":
    main()
