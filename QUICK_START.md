# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Prerequisites

#### Windows Users
1. **Install Everything**:
   - Download from: https://www.voidtools.com/
   - Install and let it index your drives (5-10 minutes)

2. **Download Everything SDK**:
   - Download from: https://www.voidtools.com/support/everything/sdk/
   - Extract the ZIP file
   - Copy `Everything64.dll` to your project's `Everything-SDK/dll/` folder

#### Linux Users
```bash
# Ubuntu/Debian
sudo apt-get install plocate && sudo updatedb

# Fedora
sudo dnf install mlocate && sudo updatedb
```

#### macOS Users
No setup required! Uses built-in Spotlight.

### Step 2: Install the MCP Server

```bash
# Recommended: Using uv
uvx mcp-server-everything-search-optimized

# Alternative: Using pip
pip install mcp-server-everything-search-optimized
```

### Step 3: Configure Claude Desktop

Add to your Claude Desktop configuration:

#### Windows Configuration
```json
{
  \"mcpServers\": {
    \"everything-search\": {
      \"command\": \"uvx\",
      \"args\": [\"mcp-server-everything-search-optimized\"],
      \"env\": {
        \"EVERYTHING_SDK_PATH\": \"C:\\\\path\\\\to\\\\Everything-SDK\\\\dll\\\\Everything64.dll\"
      }
    }
  }
}
```

#### Linux/macOS Configuration
```json
{
  \"mcpServers\": {
    \"everything-search\": {
      \"command\": \"uvx\",
      \"args\": [\"mcp-server-everything-search-optimized\"]
    }
  }
}
```

### Step 4: Test the Installation

Restart Claude Desktop and try these commands:

1. **Basic search**: \"Find all Python files\"
2. **Extension search**: \"Search for *.txt files\"
3. **Recent files**: \"Find files modified today\"

## 🔧 Troubleshooting

### Windows Issues

**\"Failed to load Everything SDK DLL\"**
- Ensure `Everything64.dll` is in `Everything-SDK/dll/`
- Check that Everything application is running
- Verify the DLL path in your configuration

**\"IPC failed (Everything service not running?)\"**
- Start the Everything application
- Check Windows Services for \"Everything\" service
- Restart Everything if needed

### Linux Issues

**\"locate command not found\"**
```bash
# Install locate/plocate
sudo apt-get install plocate  # Ubuntu/Debian
sudo dnf install mlocate      # Fedora
```

**\"Database needs to be created\"**
```bash
sudo updatedb
```

### General Issues

**\"Empty query not allowed\"**
- This is a security feature - provide a search term

**\"Query contains restricted keywords\"**
- Avoid searching for password-related terms for security

**\"Quoted string queries not supported\"**
- Use space-separated terms instead of quoted phrases

## 📚 Next Steps

- Read the [full documentation](README.md)
- Check [search syntax guide](SEARCH_SYNTAX.md)
- Review [security features](MCP_BEST_PRACTICES_IMPLEMENTATION.md)
- Run [tests](tests/) to verify functionality

## 🆘 Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/Colton-wq/mcp-everything-search-optimized/issues)
- 💬 [Discussions](https://github.com/Colton-wq/mcp-everything-search-optimized/discussions)

---

**Estimated Setup Time**: 5-10 minutes (including Everything indexing on Windows)