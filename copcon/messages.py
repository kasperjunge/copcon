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
    copconignore_path: Optional[str] = None,
    copcontarget_path: Optional[str] = None,
) -> str:
    """
    Generate the final success message for Copcon.

    Implementation of the "Option #3" approach:
      - Keep emojis and structure in the front.
      - Include a parenthetical "PS" for the GitHub star message.
    """

    # 1) Format numeric counts
    formatted_directory_count = f"{directory_count:,}"
    formatted_file_count = f"{file_count:,}"
    formatted_total_tokens = f"{total_tokens:,}"

    # 2) Build extension distribution table
    sum_tokens = sum(extension_token_map.values()) or 1
    lines = [
        "File Extension    | Tokens  |  Token Distribution",
        "-------------------------------------------",
    ]
    sorted_exts = sorted(extension_token_map.items(), key=lambda kv: kv[1], reverse=True)
    for ext, token_count in sorted_exts:
        fraction = (token_count / sum_tokens) * 100
        lines.append(f"{ext:<18}| {token_count:>6}  | {fraction:5.1f}%")
    lines.append("-------------------------------------------")
    lines.append(f"Total             | {sum_tokens:>6}  | 100.0%")

    extension_table = "\n".join(lines)

    # 3) Start assembling the message text
    base_msg = (
        "🎉 Success! Copcon has processed:\n\n"
        f"📁 {formatted_directory_count} directories\n"
        f"📄 {formatted_file_count} files\n"
        f"🔢 {formatted_total_tokens} tokens\n\n"
        f"{extension_table}\n\n"
    )

    # 4) If a .copcontarget file is in use, mention it
    if copcontarget_path:
        base_msg += f"Using `.copcontarget` from: {copcontarget_path}\n"
    # 5) If a .copconignore file is in use, mention it
    if copconignore_path:
        base_msg += f"Using `.copconignore` from: {copconignore_path}\n"

    # 6) Mention how the report is delivered
    if output_file:
        base_msg += f"\nThe report has been written to `{output_file}` 🚀\n"
    else:
        base_msg += "\nThe report has been copied to your clipboard 🚀\n"

    # 7) Parenthetical postscript for the GitHub star
    base_msg += (
        "\n(PS: If you find Copcon useful, please star it at "
        "github.com/kasperjunge/copcon ⭐️)"
    )

    return base_msg
