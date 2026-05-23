"""Dealix CLI — founder operating commands.

Lightweight argparse-based CLI used to navigate operating systems
(Brand, Proof & Content; Trust; Delivery) stored in the private
ops repo. Read-only: prints paths and reminders, never publishes.
"""

__all__ = ["main"]

from .commands import main
