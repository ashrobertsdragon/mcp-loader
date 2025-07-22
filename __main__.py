import sys


def import_add_keys(args) -> None:
    """Import and run add_keys module."""
    import add_keys

    add_keys.main(args)


def import_unload_keys(args) -> None:
    """Import and run unload module."""
    import unload_keys

    unload_keys.main(args)


def import_enable_keys(args) -> None:
    """Import and run enable module."""
    import enable_keys

    enable_keys.main(args)


def import_load_keys(args) -> None:
    """Import and run load_keys module."""
    import load_keys

    load_keys.main(args)


def print_help() -> None:
    """Print help message."""
    print("Usage: mcp_loader [load|unload|enable|add]\n")
    print("Commands:")
    print("load - Copy MCP servers from source JSON to config file.")
    print(
        "unload - Remove MCP servers from config or master MCP Servers file."
    )
    print("enable - Enable existingMCP servers in VSCode settings.json file.")
    print("add - Add MCP servers to master MCP Servers file.")
    print("\nUse mcp_loader [command] --help for more information.")


def main() -> None:
    """Main function."""
    dispatch = {
        "load": import_load_keys,
        "unload": import_unload_keys,
        "enable": import_enable_keys,
        "add": import_add_keys,
    }
    if len(sys.argv) < 2 or "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)
    if sys.argv[2] in dispatch:
        dispatch[sys.argv[2]](sys.argv[3:])


if __name__ == "__main__":
    main()
