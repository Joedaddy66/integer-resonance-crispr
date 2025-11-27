# GitHub CLI Guide for Repository Automation

This guide covers two approaches for automating GitHub repository creation and pull request workflows.

## Overview

We provide two automation scripts:

1. **`create_with_gh.sh`** — Uses GitHub CLI (`gh`) - simpler and handles auth interactively
2. **`create_with_api.sh`** — Uses GitHub REST API - suitable for CI/non-interactive environments

## Approach 1: GitHub CLI (Recommended for Interactive Use)

### Prerequisites

1. **Install GitHub CLI:**
   ```bash
   # macOS
   brew install gh

   # Ubuntu/Debian
   sudo apt install gh

   # Fedora/RHEL
   sudo dnf install gh

   # Windows (via winget)
   winget install --id GitHub.cli

   # Or see: https://cli.github.com/
   ```

2. **Authenticate:**
   ```bash
   gh auth login
   ```
   Follow the interactive prompts to authenticate via browser or token.

### Usage

```bash
# Make script executable
chmod +x create_with_gh.sh

# Run the script
./create_with_gh.sh USERNAME REPO_NAME

# Example
./create_with_gh.sh Joedaddy66 integer-resonance-crispr
```

### What the Script Does

1. Creates a new GitHub repository (public by default)
2. Initializes local git repository
3. Commits all files (README.md, analyze.py, requirements.txt, etc.)
4. Pushes to `main` branch
5. Creates feature branch (`feature/prototype-pipeline`)
6. Opens pull request from feature branch to main

### Advantages

- ✅ Simple authentication flow (interactive browser login)
- ✅ Handles SSH/HTTPS configuration automatically
- ✅ Native support for all GitHub features
- ✅ Better error messages and validation
- ✅ No token management needed

## Approach 2: GitHub REST API (For Automation/CI)

### Prerequisites

1. **Generate Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scope: `repo` (full control of private repositories)
   - Copy the token (starts with `ghp_`)

2. **Install `jq` (JSON processor):**
   ```bash
   # macOS
   brew install jq

   # Ubuntu/Debian
   sudo apt-get install jq

   # Fedora/RHEL
   sudo dnf install jq
   ```

3. **Export Token:**
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```

   **⚠️ Security Note:** Never commit tokens to git. Use environment variables or secure secret management.

### Usage

```bash
# Ensure token is exported
export GITHUB_TOKEN=ghp_your_token_here

# Make script executable
chmod +x create_with_api.sh

# Run the script
./create_with_api.sh USERNAME REPO_NAME

# Example
./create_with_api.sh Joedaddy66 integer-resonance-crispr
```

### What the Script Does

Same as `create_with_gh.sh`, but using direct API calls:
1. Creates repository via POST to `/user/repos`
2. Commits files locally
3. Pushes to remote (using token for auth)
4. Creates pull request via POST to `/repos/{owner}/{repo}/pulls`

### Advantages

- ✅ Non-interactive (suitable for CI/CD)
- ✅ Scriptable and deterministic
- ✅ Works in headless environments
- ✅ Fine-grained control over API calls

### Disadvantages

- ⚠️ Requires manual token management
- ⚠️ Token stored in git remote URL (visible in `.git/config`)
- ⚠️ More error handling needed

## Security & Best Practices

### Token Management

1. **Never commit tokens:**
   ```bash
   # ❌ BAD
   GITHUB_TOKEN=ghp_xxx ./script.sh

   # ✅ GOOD
   export GITHUB_TOKEN=ghp_xxx
   ./script.sh
   ```

2. **Use `.env` files (gitignored):**
   ```bash
   # .env (add to .gitignore!)
   GITHUB_TOKEN=ghp_xxx

   # Load before running
   source .env
   ./create_with_api.sh user repo
   ```

3. **Prefer `gh` CLI for local development** (tokens managed by gh)

### Repository Visibility

Both scripts create **public** repositories by default. To create private repos:

```bash
# create_with_gh.sh: Edit line
gh repo create "$OWNER/$REPO" --public --source=. --remote=origin

# Change to:
gh repo create "$OWNER/$REPO" --private --source=. --remote=origin
```

```bash
# create_with_api.sh: Edit JSON payload
"private": false

# Change to:
"private": true
```

## File Requirements

Both scripts assume these files exist in the current directory:
- `README.md`
- `analyze.py`
- `requirements.txt`
- `.github/workflows/ci.yml` (optional but recommended)
- `test_smoke.csv` (optional, for CI smoke tests)

If these files don't exist, the scripts will fail. Ensure all required files are present before running.

## Troubleshooting

### `gh: command not found`
Install GitHub CLI: https://cli.github.com/

### `gh auth login` fails
Try token-based auth:
```bash
gh auth login --with-token < token.txt
```

### `curl` API calls return 401 Unauthorized
- Check token is valid: `curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user`
- Ensure token has `repo` scope

### Remote URL uses HTTPS but want SSH
```bash
# After running script, change remote
git remote set-url origin git@github.com:user/repo.git
```

### Repository already exists
Both scripts fail if the repo already exists. Either:
- Delete the existing repo on GitHub
- Use a different repo name
- Manually push to existing repo

## Comparison Table

| Feature | `create_with_gh.sh` | `create_with_api.sh` |
|---------|-------------------|---------------------|
| **Auth** | Interactive browser | Token (env var) |
| **Setup** | Install `gh` + login | Install `jq` + export token |
| **CI/CD** | ❌ Not ideal | ✅ Perfect |
| **Local Dev** | ✅ Recommended | ⚠️ Token management |
| **Security** | ✅ No tokens in git | ⚠️ Token in remote URL |
| **Error Handling** | ✅ Better messages | ⚠️ Manual parsing |

## Recommended Workflow

### For Local Development
```bash
# One-time setup
brew install gh
gh auth login

# Create repos as needed
./create_with_gh.sh user repo-name
```

### For CI/CD Pipelines
```bash
# In CI environment variables
GITHUB_TOKEN=${{ secrets.GH_TOKEN }}

# Run in automation
./create_with_api.sh org repo-name
```

## Next Steps

1. Choose approach based on your environment (interactive vs. CI)
2. Install prerequisites (`gh` or `jq` + token)
3. Prepare all required files (README, analyze.py, etc.)
4. Run the appropriate script
5. Script will output the PR URL — review and merge!

## Additional Resources

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub REST API Reference](https://docs.github.com/en/rest)
- [Managing Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [Git Credential Storage](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)

## Support

For issues with these scripts:
- Check the troubleshooting section above
- Verify all prerequisites are installed
- Ensure git config is set (`user.name`, `user.email`)
- Review script output for error messages

For GitHub CLI issues:
```bash
gh --version
gh auth status
```

For API issues:
```bash
echo $GITHUB_TOKEN  # Should show ghp_...
curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user
```
