#!/usr/bin/env python3
import os
import re

def load_env(env_path=".env"):
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def replace_placeholders(template_path, env_vars):
    if not os.path.exists(template_path):
        print(f"Template not found: {template_path}")
        return

    # Determine destination file path
    target_path = template_path.replace(".template", "")

    with open(template_path, "r") as f:
        content = f.read()

    for key, value in env_vars.items():
        placeholder = f"${{{key}}}"
        content = content.replace(placeholder, value)

    with open(target_path, "w") as f:
        f.write(content)
    print(f"Generated: {target_path} (from {template_path})")

def main():
    env_vars = load_env()
    templates = [
        "dnsmasq.conf.template",
        "ztp-data/bootstrap.template",
        "arista-ztp-v2.yaml.template"
    ]

    for template_path in templates:
        replace_placeholders(template_path, env_vars)

if __name__ == "__main__":
    main()
