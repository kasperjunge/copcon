"""
Messages Module for Copcon.

This module provides functionality to build user-facing messages,
particularly the final success message shown at the end of Copcon's run.
"""

from typing import Dict, Optional

def get_success_message(
    directory_count: int,
    file_count: int,
    total_tokens: int,
    extension_token_map: Dict[str, int],
    output_file: Optional[str],
) -> str:
    """Generate the final success message for Copcon.

    Args:
        directory_count (int): Number of directories processed.
        file_count (int): Number of files processed.
        total_tokens (int): Total tokens counted in all included files.
        extension_token_map (Dict[str, int]): A mapping of file extensions
            to total tokens accounted for those extensions.
        output_file (Optional[str]): The path to which the report was written,
            if any. If None, the message indicates the report was copied to
            the clipboard.

    Returns:
        str: The finalized success message to display or echo.
    """
    # Convert numeric counts to strings with commas
    formatted_directory_count = f"{directory_count:,}"
    formatted_file_count = f"{file_count:,}"
    formatted_total_tokens = f"{total_tokens:,}"

    # ---------------------------
    # Build Extension Token Distribution Table
    # ---------------------------
    sum_tokens = sum(extension_token_map.values()) or 1  # Avoid division by zero

    lines = []
    # We REMOVED the line "File Extension Distribution (by tokens):"
    lines.append("File Extension    | Tokens  |  Token Distribution")
    lines.append("-------------------------------------------")

    # Sort by descending token count
    sorted_exts = sorted(
        extension_token_map.items(),
        key=lambda kv: kv[1],
        reverse=True
    )

    for ext, token_count in sorted_exts:
        fraction = (token_count / sum_tokens) * 100
        # Format each row
        lines.append(f"{ext:<18}| {token_count:>6}  | {fraction:5.1f}%")

    lines.append("-------------------------------------------")
    lines.append(f"Total             | {sum_tokens:>6}  | 100.0%")

    extension_table = "\n".join(lines)

    # ---------------------------
    # Build the final success message
    # ---------------------------
    if output_file:
        # If an output file was specified
        return (
            "🎉 Success! Copcon has processed:\n"
            f"📁 {formatted_directory_count} directories\n"
            f"📄 {formatted_file_count} files\n"
            f"🔢 {formatted_total_tokens} tokens\n\n"
            f"{extension_table}\n\n"
            f"The report has been written to `{output_file}`. You can now open or share it as needed. 🚀\n"
            "If you find Copcon useful, please consider leaving a star on: github.com/kasperjunge/copcon ⭐"
        )
    else:
        # If we're copying to the clipboard
        return (
            "🎉 Success! Copcon has processed:\n\n"
            f"📁 {formatted_directory_count} directories\n"
            f"📄 {formatted_file_count} files\n"
            f"🔢 {formatted_total_tokens} tokens\n\n"
            f"{extension_table}\n\n"
            "The report has been copied to your clipboard. You can now paste it into your preferred AI assistant 🚀\n\n"
            "If you find Copcon useful, please consider leaving a star on: github.com/kasperjunge/copcon ⭐"
        )
