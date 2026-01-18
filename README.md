# SynapseWatcher

**Real-time Synapse Message Notifications - No More Manual Checking!**

Watch THE_SYNAPSE folder for new messages and trigger instant callbacks. Built for AI agents who need to respond to team communication in real-time instead of polling manually every few minutes.

---

## ⚡ Features

- **Instant Detection** - 1-second poll interval (configurable)
- **Callback System** - Register multiple callback functions
- **Smart Filtering** - Priority, agent, keyword filters
- **Error Resilient** - Callback crashes don't stop watching
- **Deduplication** - Never process same message twice
- **Zero Dependencies** - Pure Python standard library
- **Cross-Platform** - Works on Windows, Linux, macOS
- **Background Mode** - Run as daemon/service

---

## 🚀 Quick Start

### Installation

```bash
# Clone or download
cd AutoProjects/SynapseWatcher

# Use immediately (no installation required!)
python synapsewatcher.py
```

### First Watch

```bash
# Watch with default callback (prints to console)
python synapsewatcher.py

# Watch for HIGH priority messages
python synapsewatcher.py --priority HIGH

# Watch for messages to specific agent
python synapsewatcher.py --to ATLAS

# Watch for urgent keywords
python synapsewatcher.py --keywords "urgent,critical,emergency"
```

---

## 💻 Usage

### Command Line Interface

```bash
# Basic watching (default: prints all new messages)
python synapsewatcher.py

# Filter by recipient
python synapsewatcher.py --to ATLAS

# Filter by sender
python synapsewatcher.py --from FORGE

# Filter by priority
python synapsewatcher.py --priority CRITICAL

# Filter by keywords (comma-separated)
python synapsewatcher.py --keywords "urgent,help,error"

# Combine filters
python synapsewatcher.py --to CLIO --priority HIGH --keywords "system"

# Custom Synapse path
python synapsewatcher.py --path "D:/custom/path/to/synapse/active"

# Adjust poll interval (seconds)
python synapsewatcher.py --interval 0.5

# Verbose logging
python synapsewatcher.py --verbose
```

### Python API

```python
from synapsewatcher import SynapseWatcher, MessageFilter
from pathlib import Path

# Create watcher
watcher = SynapseWatcher(
    synapse_path=Path("D:/BEACON_HQ/.../THE_SYNAPSE/active"),
    poll_interval=1.0  # Check every second
)

# Define callback function
def my_callback(message):
    print(f"New message from {message.from_agent}: {message.subject}")
    # Your custom logic here

# Register callback
watcher.register_callback(my_callback)

# Optional: Add filter
watcher.set_filter(MessageFilter(
    to_agent="ATLAS",
    priority="HIGH"
))

# Start watching (blocks until stopped)
watcher.start()
```

---

## 📚 Examples

### Example 1: Auto-Reply Bot

```python
from synapsewatcher import SynapseWatcher
from synapselink import quick_send

def auto_reply(message):
    if "status" in message.subject.lower():
        quick_send(
            message.from_agent,
            f"Re: {message.subject}",
            "I'm online and operational!"
        )

watcher = SynapseWatcher()
watcher.register_callback(auto_reply)
watcher.start()
```

### Example 2: Emergency Workflow Trigger

```python
from synapsewatcher import SynapseWatcher, MessageFilter

def emergency_response(message):
    print(f"[EMERGENCY] {message.subject}")
    # Trigger emergency workflow
    import subprocess
    subprocess.run(["python", "emergency_handler.py", message.msg_id])

watcher = SynapseWatcher()
watcher.set_filter(MessageFilter(priority="CRITICAL"))
watcher.register_callback(emergency_response)
watcher.start()
```

### Example 3: Task Assignment Automation

```python
from synapsewatcher import SynapseWatcher, MessageFilter

def handle_assignment(message):
    # Auto-acknowledge assignment
    from synapselink import quick_send
    quick_send(
        message.from_agent,
        f"Re: {message.subject}",
        "Assignment received! Starting work now."
    )
    
    # Create task in task queue
    create_task_from_message(message)

watcher = SynapseWatcher()
watcher.set_filter(MessageFilter(
    to_agent="BOLT",
    keywords=["assignment", "task", "build"]
))
watcher.register_callback(handle_assignment)
watcher.start()
```

**More Examples:** See [EXAMPLES.md](EXAMPLES.md) for 10+ detailed examples

---

## 🎯 Use Cases

**For AI Agents:**
- Respond to messages within seconds instead of minutes
- Trigger workflows automatically on specific messages
- Auto-acknowledge assignments
- Monitor team communication in real-time

**For Autonomous Workflows:**
- Wake up agent on CRITICAL messages
- Route tasks based on message content
- Auto-reply to status requests
- Trigger emergency response procedures

**For Team Coordination:**
- All agents notified instantly of broadcasts
- No more missed messages
- Faster collaboration cycles
- Reduced latency in multi-agent workflows

---

## 🔧 Configuration

### MessageFilter Options

```python
MessageFilter(
    to_agent="ATLAS",        # Only messages to this agent
    from_agent="FORGE",      # Only messages from this agent
    priority="HIGH",         # Only this priority (HIGH, CRITICAL, etc.)
    keywords=["urgent"]      # Only if any keyword matches
)
```

**Note:** All filters are AND conditions (all must match).

### Watcher Options

```python
SynapseWatcher(
    synapse_path=Path("/path/to/synapse/active"),  # Custom path
    poll_interval=1.0,        # Seconds between checks
    message_filter=None       # Optional MessageFilter
)
```

---

## 🛡️ Security & Reliability

**Read-Only Access:**
- SynapseWatcher only READS messages, never writes
- Safe to run alongside other Synapse tools

**Error Isolation:**
- Callback crashes don't stop the watcher
- Each callback runs in try/except block
- Errors logged but watching continues

**Deduplication:**
- Existing messages ignored on startup
- Only NEW messages trigger callbacks
- Message IDs tracked to prevent duplicates

---

## 🔄 Integration with Team Brain

### With SynapseLink

```python
from synapsewatcher import SynapseWatcher
from synapselink import quick_send, reply

def handle_mention(message):
    # Auto-reply when mentioned
    reply(
        message,
        "Thanks for the ping! I'm on it."
    )

watcher = SynapseWatcher()
watcher.set_filter(MessageFilter(to_agent="ATLAS"))
watcher.register_callback(handle_mention)
watcher.start()
```

### With TokenTracker

```python
from synapsewatcher import SynapseWatcher
from tokentracker import TokenTracker

tracker = TokenTracker()

def log_communication(message):
    # Track that we received a message
    tracker.log_usage(
        agent="ATLAS",
        model="sonnet-4.5",
        input_tokens=len(message.subject) * 4,  # Rough estimate
        output_tokens=0,
        notes=f"Received message: {message.subject}"
    )

watcher = SynapseWatcher()
watcher.register_callback(log_communication)
watcher.start()
```

### BCH Integration

In BCH chat, use:
```
@synapsewatcher start                  # Start watching
@synapsewatcher status                 # Check if running
@synapsewatcher stop                   # Stop watching
```

---

## 🐛 Troubleshooting

### No messages detected

**Cause:** Synapse path incorrect  
**Fix:** Check path with `--path` argument

### Callback not triggering

**Cause:** Filter too restrictive  
**Fix:** Remove filters and test, then add back one at a time

### High CPU usage

**Cause:** Poll interval too low  
**Fix:** Increase `--interval` (e.g., `--interval 2.0` for 2 seconds)

### Permission denied

**Cause:** No read access to Synapse folder  
**Fix:** Check file permissions on THE_SYNAPSE/active directory

---

## 📖 Documentation

- **[EXAMPLES.md](EXAMPLES.md)** - 10+ working examples
- **[CHEAT_SHEET.txt](CHEAT_SHEET.txt)** - Quick reference
- **[API Documentation](#python-api)** - Full API reference

---

## 🙏 Credits

**Built by:** Atlas (Team Brain)  
**Requested by:** Forge (Synapse infrastructure improvements)  
**For:** Logan Smith / Metaphy LLC  
**Part of:** Beacon HQ / Team Brain Ecosystem  
**Date:** January 18, 2026  
**Methodology:** Test-Break-Optimize (19/19 tests passed)

Built with ❤️ as part of the Team Brain ecosystem - where AI agents collaborate to solve real problems.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🔗 Links

- **GitHub:** https://github.com/DonkRonk17/SynapseWatcher
- **Issues:** https://github.com/DonkRonk17/SynapseWatcher/issues
- **Team Brain:** Part of the AutoProjects collection

---

**SynapseWatcher** - Because AI agents shouldn't have to manually check their inbox! ⚡
