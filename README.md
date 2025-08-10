# Everything Search MCP Server - Optimized Version

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/mamertofabian/mcp-everything-search)

An optimized MCP server that provides fast file searching capabilities across Windows, macOS, and Linux with enhanced security and performance improvements following MCP best practices.

## 🚀 Key Features

- **Cross-Platform Support**: Windows (Everything SDK), macOS (Spotlight), Linux (locate/plocate)
- **Enhanced Security**: Empty query protection, sensitive file filtering, and access controls
- **MCP Best Practices**: Optimized for AI consumption with concise error handling
- **Issue #14 Fix**: Proper handling of quoted string queries with clear error messages
- **Comprehensive Testing**: Full edge case coverage and security validation

## 🛡️ Security Improvements

- **Empty Query Protection**: Prevents system file exposure through empty queries
- **Sensitive Keyword Filtering**: Blocks searches for password-related and system files
- **Query Syntax Validation**: Rejects unsupported quoted string queries (Issue #14 fix)
- **Result Filtering**: Automatically filters sensitive files from search results
- **MCP-Compliant Error Handling**: Simple, structured error messages for AI consumption

## 📊 Performance Enhancements

- **Efficient Error Handling**: Fast validation prevents unnecessary processing
- **Optimized Filtering**: Lightweight sensitive file detection
- **Streamlined Responses**: Minimal overhead for AI model consumption
- **MCP-Optimized Architecture**: Designed for AI tool calling patterns

## 🔧 Installation

### Prerequisites

#### Windows
1. **Everything Search Application**:
   - Download and install from: https://www.voidtools.com/
   - Ensure the Everything service is running
   - Let Everything index your drives (first-time setup)

2. **Everything SDK Setup**:
   - Download Everything SDK from: https://www.voidtools.com/support/everything/sdk/
   - Extract the SDK package
   - Copy `Everything64.dll` to `Everything-SDK/dll/` in the project directory
   - Or set environment variable: `EVERYTHING_SDK_PATH=C:\\path\\to\\Everything64.dll`

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get install plocate
# or
sudo apt-get install mlocate

# Fedora
sudo dnf install mlocate

# Update database
sudo updatedb
```

#### macOS
No additional setup required (uses built-in Spotlight).

### Install via uv (Recommended)
```bash
uvx mcp-server-everything-search-optimized
```

### Install via pip
```bash
pip install mcp-server-everything-search-optimized
```

### Install from Source
```bash
git clone https://github.com/Colton-wq/mcp-everything-search-optimized.git
cd mcp-everything-search-optimized

# Setup Everything SDK (Windows only)
# Download Everything SDK and copy Everything64.dll to Everything-SDK/dll/

pip install -e .
```

## ⚙️ Configuration

### Claude Desktop Configuration

#### Windows
```json
{
  \"mcpServers\": {
    \"everything-search\": {
      \"command\": \"uvx\",
      \"args\": [\"mcp-server-everything-search-optimized\"],
      \"env\": {
        \"EVERYTHING_SDK_PATH\": \"path/to/Everything-SDK/dll/Everything64.dll\"
      }
    }
  }
}
```

#### Linux/macOS
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

## 🔍 Usage Examples

### Basic Search
```json
{
  \"query\": \"*.py\",
  \"max_results\": 50
}
```

### Advanced Windows Search
```json
{
  \"query\": \"ext:py datemodified:today\",
  \"max_results\": 10,
  \"windows_params\": {
    \"match_path\": true,
    \"sort_by\": 14
  }
}
```

### Security-Aware Search
The optimized version includes built-in filtering for sensitive directories and files.

## 🧪 Testing

Run the comprehensive test suite:
```bash
cd tests/
python -m pytest
```

### Test Coverage
- ✅ Basic functionality
- ✅ Edge cases and boundary conditions
- ✅ Security validation and filtering
- ✅ MCP best practices compliance
- ✅ Cross-platform compatibility

## 📋 API Reference

### Search Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `query` | string | Search query string | Required |
| `max_results` | integer | Maximum results (1-1000) | 100 |
| `match_path` | boolean | Match full path vs filename | false |
| `match_case` | boolean | Case-sensitive search | false |
| `match_regex` | boolean | Enable regex search | false |
| `sort_by` | integer | Sort order (Windows only) | 1 |

### Response Format
```json
{
  \"path\": \"/full/path/to/file\",
  \"filename\": \"filename.ext\",
  \"size\": 1024,
  \"created\": \"2025-08-10T12:00:00Z\",
  \"modified\": \"2025-08-10T12:00:00Z\",
  \"accessed\": \"2025-08-10T12:00:00Z\"
}
```

### Search Syntax Guide

For detailed information about the search syntax supported on each platform (Windows, macOS, and Linux), please see [SEARCH_SYNTAX.md](SEARCH_SYNTAX.md).

## 🐛 Known Issues & Fixes

- **Issue #14**: Quoted string queries - Now properly rejected with clear error
- **Empty Query Security**: Prevents system file exposure with validation
- **Sensitive File Access**: Automatic filtering of password and system files
- **MCP Compliance**: Error handling optimized for AI model consumption

## 🔒 Security Features

### Input Validation
- Empty query detection and rejection
- Sensitive keyword filtering
- Quoted string query validation
- Malformed input handling

### Result Filtering
- Automatic sensitive file removal
- System directory protection
- Password-related file blocking
- Configurable sensitivity levels

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `python -m pytest tests/`
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original project by [mamertofabian](https://github.com/mamertofabian/mcp-everything-search)
- Everything SDK by [voidtools](https://www.voidtools.com/)
- MCP Protocol by [Anthropic](https://github.com/modelcontextprotocol)

## 📞 Support

- 📖 [Documentation](CHANGELOG.md)
- 🐛 [Issue Tracker](https://github.com/Colton-wq/mcp-everything-search-optimized/issues)
- 💬 [Discussions](https://github.com/Colton-wq/mcp-everything-search-optimized/discussions)

---

**Note**: This is an optimized version with security and performance improvements following MCP best practices. For the original version, see [mamertofabian/mcp-everything-search](https://github.com/mamertofabian/mcp-everything-search).