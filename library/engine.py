"""Library Circulation & Cataloging Engine for Frappe Framework."""

from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class Book(BaseModel):
    isbn: str
    title: str
    author: str
    total_copies: int = 1
    available_copies: int = 1


class Member(BaseModel):
    member_id: str
    name: str
    membership_type: str = "Standard"  # Standard (max 2 books), Premium (max 5 books)
    max_allowed_books: int = 2
    active_loans_count: int = 0


class LoanRecord(BaseModel):
    loan_id: str
    isbn: str
    member_id: str
    issue_date: str  # YYYY-MM-DD
    due_date: str
    return_date: Optional[str] = None
    fine_amount: float = 0.0


class LibraryEngine:
    """Manages book circulation, loans, and automated late fine calculation."""

    DAILY_FINE_RATE = 5.0  # ₹5 per day late fine

    def __init__(self):
        self.catalog: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}
        self.loans: Dict[str, LoanRecord] = {}

    def issue_book(self, isbn: str, member_id: str, loan_duration_days: int = 14) -> LoanRecord:
        if isbn not in self.catalog:
            raise ValueError(f"Book with ISBN {isbn} not found in catalog")
        if member_id not in self.members:
            raise ValueError(f"Member {member_id} not registered")

        book = self.catalog[isbn]
        member = self.members[member_id]

        if book.available_copies <= 0:
            raise ValueError("No copies currently available for issue")
        if member.active_loans_count >= member.max_allowed_books:
            raise ValueError(f"Member has reached maximum loan limit ({member.max_allowed_books})")

        issue_dt = date.today()
        due_dt = issue_dt + timedelta(days=loan_duration_days)
        loan_id = f"LOAN-{len(self.loans) + 1:04d}"

        loan = LoanRecord(
            loan_id=loan_id,
            isbn=isbn,
            member_id=member_id,
            issue_date=issue_dt.strftime("%Y-%m-%d"),
            due_date=due_dt.strftime("%Y-%m-%d"),
        )

        book.available_copies -= 1
        member.active_loans_count += 1
        self.loans[loan_id] = loan
        return loan

    def return_book(self, loan_id: str, return_date_str: Optional[str] = None) -> Dict[str, Any]:
        if loan_id not in self.loans:
            raise ValueError("Loan record not found")

        loan = self.loans[loan_id]
        if loan.return_date:
            raise ValueError("Book has already been returned")

        ret_dt = (
            datetime.strptime(return_date_str, "%Y-%m-%d").date()
            if return_date_str
            else date.today()
        )
        due_dt = datetime.strptime(loan.due_date, "%Y-%m-%d").date()

        days_overdue = max(0, (ret_dt - due_dt).days)
        fine = days_overdue * self.DAILY_FINE_RATE

        loan.return_date = ret_dt.strftime("%Y-%m-%d")
        loan.fine_amount = fine

        # Restore inventory
        if loan.isbn in self.catalog:
            self.catalog[loan.isbn].available_copies += 1
        if loan.member_id in self.members:
            self.members[loan.member_id].active_loans_count -= 1

        return {
            "loan_id": loan_id,
            "days_overdue": days_overdue,
            "fine_amount": fine,
            "status": "Returned",
        }
