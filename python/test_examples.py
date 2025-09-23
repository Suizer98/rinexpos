def black_formatting_issues():
    """This function will FAIL Black formatting checks"""
    # Add random spaces and line breaks to test black formatting
    x = 1 + 2 * 3
    y = {"a": 1, "b": 2, "c": 3}
    z = (
        "hello"
        + "world"
        + "this"
        + "is"
        + "a"
        + "very"
        + "long"
        + "string"
        + "that"
        + "exceeds"
        + "the"
        + "line"
        + "limit"
        + "and"
        + "should"
        + "be"
        + "reformatted"
    )
    return x, y, z


def ruff_linting_issues():
    """This function will FAIL Ruff linting checks"""
    # Uncomment this to test unused imports
    # import os

    # Unused variables
    unused_var = "never used"

    # Comparison with None using ==
    if unused_var is None:
        pass

    # Mutable default argument
    def bad_function(items=None):
        if items is None:
            items = []
        items.append("bad")
        return items

    return "hello"


# def bandit_security_issues():
#     """This function will FAIL Bandit security checks"""
#     import os

#     # Test ONLY os.system() command injection (B605) - HIGH SEVERITY
#     user_input = "malicious_command"
#     os.system(f"echo {user_input}")

#     return


# def safety_dependency_issues():
#     """This function uses potentially vulnerable dependencies"""
#     # Install older requests version to test Safety
#     import requests

#     response = requests.get("https://example.com")
#     return response.text


# def semgrep_security_issues():
#     """This function will FAIL Semgrep security checks"""
#     import json
#     import re
#     import sqlite3
#     import urllib.request
#     import os
#     import subprocess

#     # SQL injection - more explicit pattern
#     user_input = "1; DROP TABLE users; --"
#     query = "SELECT * FROM users WHERE id = " + user_input
#     conn = sqlite3.connect(":memory:")
#     cursor = conn.cursor()
#     cursor.execute(query)

#     # Command injection
#     user_cmd = "rm -rf /"
#     os.system("echo " + user_cmd)
#     subprocess.run("ls " + user_cmd, shell=True)

#     # Path traversal - more explicit
#     filename = "../../../etc/passwd"
#     with open(filename, "r") as f:
#         content = f.read()

#     # XSS - more explicit
#     user_input = "<script>alert('xss')</script>"
#     html = "<div>" + user_input + "</div>"

#     # Unsafe URL opening
#     url = "http://example.com/data"
#     response = urllib.request.urlopen(url)

#     # Unsafe JSON parsing
#     json_string = '{"malicious": "data"}'
#     data = json.loads(json_string)

#     # ReDoS - more explicit
#     pattern = r"(a+)+$"
#     re.match(pattern, "aaaaaaaaaaaaaaaaaaaa!")

#     # eval() usage
#     user_code = "os.system('rm -rf /')"
#     eval(user_code)

#     # exec() usage
#     exec(user_code)

#     return content, html, data


# def semgrep_secrets_issues():
#     """This function will FAIL Semgrep secrets detection"""
#     # Hardcoded API keys - more explicit patterns
#     openai_key = "sk-1234567890abcdef1234567890abcdef"
#     aws_access_key = "AKIAIOSFODNN7EXAMPLE"
#     aws_secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
#     github_token = "ghp_1234567890abcdef1234567890abcdef12345678"
#     slack_token = "xoxb-1234567890-1234567890-1234567890-1234567890abcdef"

#     # Hardcoded passwords
#     db_password = "super_secret_password_123"
#     jwt_secret = "my-super-secret-jwt-key"
#     api_secret = "secret123456789"

#     # Database URLs with credentials
#     database_url = "postgresql://user:password@localhost/db"
#     redis_url = "redis://:password@localhost:6379/0"

#     # Private keys
#     private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC..."
#     rsa_key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA..."

#     return {
#         "openai_key": openai_key,
#         "aws_access_key": aws_access_key,
#         "aws_secret_key": aws_secret_key,
#         "github_token": github_token,
#         "slack_token": slack_token,
#         "db_password": db_password,
#         "jwt_secret": jwt_secret,
#         "api_secret": api_secret,
#         "database_url": database_url,
#         "redis_url": redis_url,
#         "private_key": private_key,
#         "rsa_key": rsa_key,
#     }


def risky_operation():
    """Helper function for testing"""
    return 1 / 0


if __name__ == "__main__":
    print("Tool-specific test file!")
    print("Comment out functions to test individual tools:")
    print("- black_formatting_issues() -> Test Black")
    print("- ruff_linting_issues() -> Test Ruff")
    print("- bandit_security_issues() -> Test Bandit")
    print("- safety_dependency_issues() -> Test Safety")
    print("- semgrep_security_issues() -> Test Semgrep")
    print("- semgrep_secrets_issues() -> Test Semgrep Secrets")
