# mcp-loader

Easily modify MCP configuration files with a simple CLI using a master list.

## Overview

`mcp-loader` is a command-line interface (CLI) tool designed to streamline the management of MCP (Multi-Client Protocol) server configurations. It allows users to add, load, unload, and enable/disable MCP server entries in various JSON configuration files, including VSCode's `settings.json`, using a centralized master list.

## Features

*   **`load`**: Copy MCP server configurations from a source JSON file (your master list) to a destination configuration file.
*   **`unload`**: Remove or disable MCP server configurations from a target JSON file.
*   **`enable`**: Enable previously disabled MCP server configurations within a VSCode `settings.json` file.
*   **`add`**: Add new MCP server configurations to your master MCP servers file.

## Installation

To install `mcp-loader`, clone the repository and use `uv`:

```bash
git clone YOUR_GITHUB_REPO_URL_HERE
cd mcp_loader
uv pip install .
```

This will install the `mcp-loader` package and make the `add-mcp`, `enable-mcp`, `load-mcp`, `mcp-loader`, and `unload-mcp` commands available in your system's PATH.

## Usage

The preferred way to use `mcp-loader` is through its individual command-line scripts:

*   `add-mcp`
*   `enable-mcp`
*   `load-mcp`
*   `unload-mcp`

Each command provides its own help message:

```bash
<command> --help
```

### General Options

All commands support the following options:

*   `-d`, `--dry-run`: Run in dry-run mode to preview changes without writing to the file.
*   `-v`, `--verbose`: Increase logging verbosity (e.g., `-v` for WARNING, `-vv` for INFO).
*   `<config_path>`: The absolute path to the target configuration file (e.g., `/path/to/settings.json`).

### `load-mcp`

Copies MCP servers from a source JSON file to a destination configuration file.

```bash
load-mcp /path/to/source_master.json /path/to/destination_config.json SERVER1 [SERVER2 ...]
```

*   `/path/to/source_master.json`: Path to your master MCP Servers file.
*   `/path/to/destination_config.json`: Path to the destination configuration file (e.g., `settings.json`).
*   `SERVER1 [SERVER2 ...]`: One or more server names to load from the source file.

### `unload-mcp`

Removes or disables MCP servers from a configuration file.

```bash
unload-mcp /path/to/config.json SERVER1 [SERVER2 ...] [--disable]
```

*   `/path/to/config.json`: Path to the configuration file.
*   `SERVER1 [SERVER2 ...]`: One or more server names to unload.
*   `--disable`: (Optional) If specified, servers will be marked as `disabled: true` instead of being completely removed from the file (primarily for VSCode `settings.json`).

### `enable-mcp`

Enables existing MCP servers in a VSCode `settings.json` file.

```bash
enable-mcp /path/to/settings.json SERVER1 [SERVER2 ...]
```

*   `/path/to/settings.json`: Path to your VSCode `settings.json` file.
*   `SERVER1 [SERVER2 ...]`: One or more server names to enable.

### `add-mcp`

Adds new MCP server configurations to your master MCP servers file. You can define multiple servers in a single command by repeating the `--server` argument and its associated options.

```bash
add-mcp <master_servers_file> \
  --server SERVER_NAME_1 (--command "your_command" | --url "http://your-url.com") \
  [--type {stio,sse,http}] \
  [--args "arg1" "arg2" ...] \
  [--headers "Key=Value" "Key2=Value2" ...] \
  [--env "VAR=value" "VAR2=value2" ...] \
  [--cwd "/path/to/working/directory"] \
  [--timeout SECONDS] \
  [--disabled] \
  [--auto-approve "tool1" "tool2" ...] \
  [--server SERVER_NAME_2 ...]
```

*   `<master_servers_file>`: The absolute path to your master MCP Servers file (e.g., `/path/to/master_servers.json`).

*   `--server SERVER_NAME`: **Required**. The unique name for the MCP server configuration.

*   `--command "your_command"`: **Mutually exclusive with `--url`**. Specifies the command to execute when this server is activated. This is typically used for local development servers or scripts.

*   `--url "http://your-url.com"` (or `--http-url`): **Mutually exclusive with `--command`**. Specifies the URL to connect to a remote server. This is commonly used for HTTP/HTTPS based MCP servers.

*   `--type {stio,sse,http}`: (Optional) Defines the transport type for the server connection. Valid options are:
    *   `stio`: Socket.IO transport.
    *   `sse`: Server-Sent Events transport.
    *   `http`: Standard HTTP/HTTPS transport.

*   `--args "arg1" "arg2" ...`: (Optional) A list of arguments to pass to the `--command` or `--url` when the server is run. These are typically command-line arguments for an executable or query parameters for a URL.

*   `--headers "Key=Value" "Key2=Value2" ...`: (Optional) For HTTP/HTTPS servers, a list of HTTP headers to include in requests, specified as key-value pairs (e.g., `"Authorization=Bearer token"`).

*   `--env "VAR=value" "VAR2=value2" ...`: (Optional) A list of environment variables to set for the process when the `--command` is executed, specified as key-value pairs (e.g., `"NODE_ENV=development"`).

*   `--cwd "/path/to/working/directory"`: (Optional) Sets the current working directory for the process when the `--command` is executed.

*   `--timeout SECONDS`: (Optional) An integer representing the timeout in seconds for the server connection or command execution.

*   `--disabled`: (Optional) A boolean flag. If present, the server configuration will be initially marked as disabled. This is useful for temporarily deactivating a server without removing its configuration.

*   `--auto-approve "tool1" "tool2" ...`: (Optional) A list of tools that should be automatically approved when interacting with this server.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

