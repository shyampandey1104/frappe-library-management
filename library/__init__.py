"""Frappe Library Management System."""

from library.engine import LibraryEngine, Book, Member, LoanRecord

__version__ = "1.0.0"
__all__ = ["LibraryEngine", "Book", "Member", "LoanRecord"]
