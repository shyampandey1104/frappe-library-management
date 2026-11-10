"""Unit tests for LibraryEngine."""

from library.engine import LibraryEngine, Book, Member


def test_issue_and_late_fine_return():
    engine = LibraryEngine()
    book = Book(isbn="978-0132350884", title="Clean Code", author="Robert C. Martin", total_copies=2, available_copies=2)
    member = Member(member_id="MEM-001", name="Rahul Verma", max_allowed_books=2)

    engine.catalog[book.isbn] = book
    engine.members[member.member_id] = member

    # Issue book
    loan = engine.issue_book(book.isbn, member.member_id, loan_duration_days=14)
    assert loan.isbn == book.isbn
    assert engine.catalog[book.isbn].available_copies == 1
    assert engine.members[member.member_id].active_loans_count == 1

    # Return book 5 days late
    res = engine.return_book(loan.loan_id, return_date_str="2026-11-29")
    assert res["status"] == "Returned"
    assert engine.catalog[book.isbn].available_copies == 2
    assert engine.members[member.member_id].active_loans_count == 0
