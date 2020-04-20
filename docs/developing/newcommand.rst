####################
Adding a new command
####################

1. Edit setup.cfg
2. Create a Github issue to track the work
3. Implement the command logic
4. Implement at least basic unit tests for helper functions 
5. Write any supplemental or non-automated documentation

*********
Setup.cfg
*********

Edit contents of ``setup.cfg`` to include the command and a pointer to a stub class

************
GitHub Issue
************

Install the current build in **editable** mode ``pip install -e .``. Now, run the 
script ``python scripts/github-create-issues.py``.

The **github-create-issues** script requires environment variable 
``GITHUB_API_KEY`` to be set to an API key that is authorized to manage the 
``tapis-cli`` repository, as it will be creating and tagging new issues. 

