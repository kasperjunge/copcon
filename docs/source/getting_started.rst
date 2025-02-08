Getting Started with Copcon
============================

Introduction
------------

Welcome to Copcon! This guide will walk you through installing and using Copcon—a CLI tool that generates a detailed report of your project's directory structure and file contents. Whether you need context for an AI chatbot or simply want to document your project, Copcon makes it easy.

Installation
------------

Before you begin, ensure you have Python 3.11 or later installed. Then, install Copcon using pip:

.. code-block:: bash

    pip install copcon

Basic Usage
-----------

After installation, you can run Copcon directly from your terminal. The most basic usage is as follows:

.. code-block:: bash

    copcon /path/to/your/project

This command generates a report of your project and copies it directly to your clipboard.

Step-by-Step Guide
------------------

1. **Navigate to Your Project Directory**

   Open your terminal and change to the directory where your project is located:

   .. code-block:: bash

       cd /path/to/your/project

2. **Generate a Report and Copy to Clipboard**

   Run the command below to generate a report of your project. The report will automatically be copied to your clipboard:

   .. code-block:: bash

       copcon .

3. **Limit Directory Traversal Depth**

   If you want to limit how deep Copcon traverses your directory structure, use the ``--depth`` option. For example, to traverse only two levels deep:

   .. code-block:: bash

       copcon . --depth 2

4. **Control Hidden Files and Directories**

   By default, Copcon excludes hidden files and directories. If you wish to include them, use the ``--no-exclude-hidden`` flag:

   .. code-block:: bash

       copcon . --no-exclude-hidden

5. **Using Ignore Patterns**

   Copcon automatically applies ignore patterns from a ``.copconignore`` file (using gitignore syntax). If no such file is found, internal default patterns are used. Customize this file in your project to exclude specific files or directories.

6. **Output the Report to a File**

   Instead of copying the report to your clipboard, you can save it to a file using the ``--output-file`` option:

   .. code-block:: bash

       copcon . --output-file report.txt

7. **Include Git Diff in the Report**

   To append the output of ``git diff`` (showing changes since the last commit) to your report, use the ``-g`` or ``--git-diff`` flag:

   .. code-block:: bash

       copcon . --git-diff

   The git diff output will be appended at the end of the report, and its token count will be included in the summary.

Summary
-------

Copcon is a powerful tool that simplifies generating detailed project reports. With flexible options for depth control, hidden file handling, ignore patterns, file output, and git diff integration, it’s designed to fit a wide range of workflows.

Next Steps
----------

For further details, check out the following sections:
- **CLI Documentation:** See :doc:`cli` for complete command options.
- **Core Modules:** See :doc:`core/index` for advanced topics such as file filtering, report formatting, and more.
- **Utilities:** See :doc:`utils/index` for additional tools and logging details.

Happy coding!
