import pytest
from copcon.messages import get_success_message

def test_get_success_message_with_output_file():
    """
    Test that the success message is generated correctly
    when an output file path is provided.
    """
    directory_count = 3
    file_count = 10
    total_tokens = 1234
    extension_token_map = {
        ".py": 800,
        ".txt": 300,
        "(no extension)": 134
    }
    output_file = "some_report.txt"

    message = get_success_message(
        directory_count=directory_count,
        file_count=file_count,
        total_tokens=total_tokens,
        extension_token_map=extension_token_map,
        output_file=output_file
    )

    # Basic checks that critical data is in the message
    assert "3 directories" in message
    assert "10 files" in message
    assert "1,234 tokens" in message
    assert "some_report.txt" in message  # The output file name
    assert "(no extension)" in message   # The extension label
    assert ".py" in message
    assert ".txt" in message
    assert "File Extension" in message
    assert "Token Distribution" in message

    # We should see "The report has been written to"
    assert "The report has been written to" in message


def test_get_success_message_no_output_file():
    """
    Test that the success message is generated correctly
    for the clipboard scenario (no output file).
    """
    directory_count = 5
    file_count = 15
    total_tokens = 999
    extension_token_map = {
        ".tar.gz": 500,
        ".py": 499
    }
    output_file = None

    message = get_success_message(
        directory_count=directory_count,
        file_count=file_count,
        total_tokens=total_tokens,
        extension_token_map=extension_token_map,
        output_file=output_file
    )

    # Verify the message includes the relevant info
    assert "5 directories" in message
    assert "15 files" in message
    assert "999 tokens" in message
    assert ".tar.gz" in message
    assert ".py" in message
    assert "File Extension" in message
    assert "Token Distribution" in message

    # We should see "The report has been copied to your clipboard" for the clipboard version
    assert "report has been copied to your clipboard" in message
    # Confirm we do not mention the file
    assert "The report has been written to" not in message


def test_get_success_message_empty_extensions():
    """
    Test that the success message handles an empty extension_token_map gracefully.
    """
    directory_count = 0
    file_count = 0
    total_tokens = 0
    extension_token_map = {}
    output_file = None

    message = get_success_message(
        directory_count=directory_count,
        file_count=file_count,
        total_tokens=total_tokens,
        extension_token_map=extension_token_map,
        output_file=output_file
    )

    assert "0 directories" in message
    assert "0 files" in message
    assert "0 tokens" in message
    assert "File Extension" in message
    assert "Token Distribution" in message
    # The table should be present but have 'Total' row at least
    assert "Total" in message
    # Because no output_file => the message should mention clipboard
    assert "report has been copied to your clipboard" in message
