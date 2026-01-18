#!/usr/bin/env python3
"""
SynapseWatcher v1.0 - Real-time Synapse Message Notifications

Monitors THE_SYNAPSE folder for new messages and triggers callbacks automatically.
No more manual checking - get instant notifications when messages arrive!

Author: Atlas (Team Brain)
Requested by: Forge
Date: January 18, 2026
"""

import json
import time
import signal
import sys
from pathlib import Path
from typing import Callable, List, Optional, Set, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import logging

VERSION = "1.0.0"

# Default Synapse path
DEFAULT_SYNAPSE_PATH = Path("D:/BEACON_HQ/MEMORY_CORE_V2/03_INTER_AI_COMMS/THE_SYNAPSE/active")


@dataclass
class SynapseMessage:
    """Represents a Synapse message."""
    msg_id: str
    from_agent: str
    to: List[str]
    subject: str
    body: Dict[str, Any]
    priority: str
    timestamp: str
    filepath: Path
    
    @classmethod
    def from_file(cls, filepath: Path) -> 'SynapseMessage':
        """Load a message from a JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls(
            msg_id=data.get('msg_id', data.get('message_id', 'unknown')),
            from_agent=data.get('from', data.get('from_agent', 'UNKNOWN')),
            to=data.get('to', []),
            subject=data.get('subject', ''),
            body=data.get('body', {}),
            priority=data.get('priority', 'NORMAL'),
            timestamp=data.get('timestamp', ''),
            filepath=filepath
        )


class MessageFilter:
    """Filter messages based on criteria."""
    
    def __init__(self,
                 to_agent: Optional[str] = None,
                 from_agent: Optional[str] = None,
                 priority: Optional[str] = None,
                 keywords: Optional[List[str]] = None):
        """
        Initialize message filter.
        
        Args:
            to_agent: Only match messages sent to this agent
            from_agent: Only match messages from this agent
            priority: Only match this priority level
            keywords: Only match if any keyword appears in subject/body
        """
        self.to_agent = to_agent
        self.from_agent = from_agent
        self.priority = priority
        self.keywords = keywords or []
    
    def matches(self, message: SynapseMessage) -> bool:
        """Check if message matches filter criteria."""
        
        # Check to_agent
        if self.to_agent:
            # Handle both string and list formats
            to_list = message.to if isinstance(message.to, list) else [message.to]
            if self.to_agent not in to_list and "ALL_AGENTS" not in to_list and "ALL" not in to_list:
                return False
        
        # Check from_agent
        if self.from_agent and message.from_agent != self.from_agent:
            return False
        
        # Check priority
        if self.priority and message.priority != self.priority:
            return False
        
        # Check keywords
        if self.keywords:
            body_text = json.dumps(message.body) if isinstance(message.body, dict) else str(message.body)
            text = (message.subject + " " + body_text).lower()
            if not any(kw.lower() in text for kw in self.keywords):
                return False
        
        return True


class SynapseWatcher:
    """
    Watches THE_SYNAPSE folder for new messages and triggers callbacks.
    
    Usage:
        watcher = SynapseWatcher()
        watcher.register_callback(my_callback_function)
        watcher.start()
    """
    
    def __init__(self,
                 synapse_path: Optional[Path] = None,
                 poll_interval: float = 1.0,
                 message_filter: Optional[MessageFilter] = None):
        """
        Initialize SynapseWatcher.
        
        Args:
            synapse_path: Path to THE_SYNAPSE/active folder
            poll_interval: How often to check for new messages (seconds)
            message_filter: Optional filter for messages
        """
        self.synapse_path = synapse_path or DEFAULT_SYNAPSE_PATH
        self.poll_interval = poll_interval
        self.message_filter = message_filter
        
        self.callbacks: List[Callable[[SynapseMessage], None]] = []
        self.seen_messages: Set[str] = set()
        self.running = False
        
        # Setup logging
        self.logger = logging.getLogger('SynapseWatcher')
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(handler)
        
        # Validate synapse path
        if not self.synapse_path.exists():
            raise FileNotFoundError(f"Synapse path does not exist: {self.synapse_path}")
        if not self.synapse_path.is_dir():
            raise NotADirectoryError(f"Synapse path is not a directory: {self.synapse_path}")
    
    def register_callback(self, callback: Callable[[SynapseMessage], None]):
        """
        Register a callback function to be called on new messages.
        
        Args:
            callback: Function that takes a SynapseMessage as argument
        """
        self.callbacks.append(callback)
        self.logger.info(f"Registered callback: {callback.__name__}")
    
    def set_filter(self, message_filter: MessageFilter):
        """Set the message filter."""
        self.message_filter = message_filter
        self.logger.info(f"Filter set: {message_filter.__dict__}")
    
    def _detect_new_messages(self) -> List[Path]:
        """Detect new message files that haven't been seen yet."""
        new_messages = []
        
        try:
            for filepath in self.synapse_path.glob("*.json"):
                msg_id = filepath.stem
                if msg_id not in self.seen_messages:
                    new_messages.append(filepath)
                    self.seen_messages.add(msg_id)
        except Exception as e:
            self.logger.error(f"Error detecting new messages: {e}")
        
        return new_messages
    
    def _process_message(self, filepath: Path):
        """Process a newly detected message."""
        try:
            # Load message
            message = SynapseMessage.from_file(filepath)
            
            # Apply filter
            if self.message_filter and not self.message_filter.matches(message):
                self.logger.debug(f"Message {message.msg_id} filtered out")
                return
            
            # Log event
            self.logger.info(f"NEW MESSAGE: {message.msg_id} from {message.from_agent} - {message.subject}")
            
            # Execute callbacks
            for callback in self.callbacks:
                try:
                    callback(message)
                except Exception as e:
                    self.logger.error(f"Callback {callback.__name__} error: {e}")
        
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in {filepath.name}: {e}")
        except Exception as e:
            self.logger.error(f"Error processing {filepath.name}: {e}")
    
    def _watch_loop(self):
        """Main watching loop."""
        self.logger.info(f"Watching: {self.synapse_path}")
        self.logger.info(f"Poll interval: {self.poll_interval}s")
        self.logger.info(f"Callbacks registered: {len(self.callbacks)}")
        
        # Initial scan to mark existing messages as seen
        for filepath in self.synapse_path.glob("*.json"):
            self.seen_messages.add(filepath.stem)
        self.logger.info(f"Marked {len(self.seen_messages)} existing messages as seen")
        
        while self.running:
            try:
                # Detect new messages
                new_messages = self._detect_new_messages()
                
                # Process each new message
                for filepath in new_messages:
                    self._process_message(filepath)
                
                # Sleep until next poll
                time.sleep(self.poll_interval)
            
            except KeyboardInterrupt:
                self.logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                self.logger.error(f"Error in watch loop: {e}")
                time.sleep(self.poll_interval)
    
    def start(self):
        """Start watching for new messages."""
        if self.running:
            self.logger.warning("Already running!")
            return
        
        if not self.callbacks:
            self.logger.warning("No callbacks registered! Add callbacks before starting.")
        
        self.running = True
        self.logger.info("SynapseWatcher started")
        
        try:
            self._watch_loop()
        finally:
            self.running = False
            self.logger.info("SynapseWatcher stopped")
    
    def stop(self):
        """Stop watching."""
        self.logger.info("Stop requested")
        self.running = False


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SynapseWatcher - Real-time Synapse message notifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Watch with simple callback
  python synapsewatcher.py --callback "print('New message!')"
  
  # Watch for HIGH priority messages to ATLAS
  python synapsewatcher.py --to ATLAS --priority HIGH
  
  # Watch for urgent keywords
  python synapsewatcher.py --keywords "urgent,critical,emergency"
        """
    )
    
    parser.add_argument('--path', type=str, default=str(DEFAULT_SYNAPSE_PATH),
                        help='Path to THE_SYNAPSE/active folder')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Poll interval in seconds (default: 1.0)')
    parser.add_argument('--to', type=str,
                        help='Filter: Only show messages to this agent')
    parser.add_argument('--from', dest='from_agent', type=str,
                        help='Filter: Only show messages from this agent')
    parser.add_argument('--priority', type=str,
                        help='Filter: Only show this priority (HIGH, CRITICAL, etc.)')
    parser.add_argument('--keywords', type=str,
                        help='Filter: Only show messages with these keywords (comma-separated)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose logging')
    parser.add_argument('--version', action='version', version=f'SynapseWatcher {VERSION}')
    
    args = parser.parse_args()
    
    # Setup logging level
    if args.verbose:
        logging.getLogger('SynapseWatcher').setLevel(logging.DEBUG)
    
    # Build filter
    message_filter = None
    if any([args.to, args.from_agent, args.priority, args.keywords]):
        keywords = args.keywords.split(',') if args.keywords else None
        message_filter = MessageFilter(
            to_agent=args.to,
            from_agent=args.from_agent,
            priority=args.priority,
            keywords=keywords
        )
    
    # Create watcher
    try:
        watcher = SynapseWatcher(
            synapse_path=Path(args.path),
            poll_interval=args.interval,
            message_filter=message_filter
        )
    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Default callback: print to console
    def default_callback(message: SynapseMessage):
        print(f"\n{'='*80}")
        print(f"[NEW MESSAGE] {message.msg_id}")
        print(f"From: {message.from_agent}")
        print(f"To: {', '.join(message.to)}")
        print(f"Priority: {message.priority}")
        print(f"Subject: {message.subject}")
        print(f"Time: {message.timestamp}")
        print(f"{'='*80}\n")
    
    watcher.register_callback(default_callback)
    
    # Handle shutdown gracefully
    def signal_handler(signum, frame):
        print("\nShutting down gracefully...")
        watcher.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start watching
    print(f"SynapseWatcher v{VERSION}")
    print(f"Watching: {args.path}")
    if message_filter:
        print(f"Filters active: {message_filter.__dict__}")
    print("Press Ctrl+C to stop\n")
    
    watcher.start()


if __name__ == "__main__":
    main()
