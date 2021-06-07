# Contributing

## Pull Request Process

1. Ensure your local environment is set.
   1. Clone your own fork of this repo
   2. Activate a python3.7 virtualenv
   3. Code
2. Update the `docs/` related to your changes, if required.
3. Update `example/` (editing or adding a new one related to your changes)
4. Ensure tests are passing (`make test` or `make test-cov`)
   1. This project uses `pre-commit` and `Black` for code styling and adequacy tests. ( try `make setup-pre-commit`)
5. Commit, Push and make a Pull Request!


### Common Workflow:

```bash
# clone your fork of this repo
git clone git@github.com:{$USER}/site_checker.git

# Add the upstream remote
git remote add upstream https://github.com/<org>/<repo>.git

# Activate your Python Environment
python3.7 -m venv .venv
source .venv/bin/activate

# Install development dependencies
make setup-pre-commit
make dev

# Checkout to a working branch
git checkout -b my_feature

# Open your favorite editor (VSCode for example)
code .

# After editing please rebase with upstream
git fetch upstream; git rebase upstream/master
# Fix any conflicts if any.

# Update docs/ if needed
# Edit example/ if needed

# Then ensure tests are ok
make test

# Now commit your changes
git commit -am "Changed XPTO to fix #issue_number"

# Push to your own fork
git push -u origin HEAD

# Open github.com/<org>/<repo> and send a Pull Request.
```
