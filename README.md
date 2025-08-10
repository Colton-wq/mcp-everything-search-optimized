# Everything Search MCP Server - Optimized Version

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/mamertofabian/mcp-everything-search)

An optimized MCP server that provides fast file searching capabilities across Windows, macOS, and Linux with enhanced security and performance improvements.

## 🚀 Key Features

- **Cross-Platform Support**: Windows (Everything SDK), macOS (Spotlight), Linux (locate/plocate)
- **Enhanced Security**: Sensitive file filtering and access controls
- **Performance Optimized**: Intelligent result limiting and caching
- **Comprehensive Testing**: Full edge case coverage and validation
- **Improved Error Handling**: Clear error messages and validation

## 🔧 Installation

### Prerequisites

#### Windows
- [Everything search utility](https://www.voidtools.com/) (service running)
- [Everything SDK](https://www.voidtools.com/support/everything/sdk/) (extracted)

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
uvx mcp-server-everything-search
```

### Install via pip
```bash
pip install mcp-server-everything-search
```

## ⚙️ Configuration

### Claude Desktop Configuration

#### Windows
```json
{
  "mcpServers": {
    "everything-search": {
      "command": "uvx",
      "args": ["mcp-server-everything-search"],
      "env": {
        "EVERYTHING_SDK_PATH": "path/to/Everything-SDK/dll/Everything64.dll"
      }
    }
  }
}
```

#### Linux/macOS
```json
{
  "mcpServers": {
    "everything-search": {
      "command": "uvx",
      "args": ["mcp-server-everything-search"]
    }
  }
}
```

## 🔍 Usage Examples

### Basic Search
```json
{
  "query": "*.py",
  "max_results": 50
}
```

### Advanced Windows Search
```json
{
  "query": "ext:py datemodified:today",
  "max_results": 10,
  "windows_params": {
    "match_path": true,
    "sort_by": 14
  }
}
```

### Security-Aware Search
The optimized version includes built-in filtering for sensitive directories and files.

## 🛡️ Security Improvements

- **Sensitive File Filtering**: Automatically excludes password files and system directories
- **Query Validation**: Prevents empty queries and malformed inputs
- **Access Control**: Respects system permissions and security boundaries
- **Audit Logging**: Optional logging of search activities

## 📊 Performance Enhancements

- **Smart Result Limiting**: Dynamic limits based on query complexity
- **Caching**: Intelligent caching for frequently accessed results
- **Memory Management**: Optimized memory usage for large result sets
- **Response Time Optimization**: Sub-second response for most queries

## 🧪 Testing

Run the comprehensive test suite:
```bash
cd tests/
python -m pytest
```

### Test Coverage
- ✅ Basic functionality
- ✅ Edge cases and boundary conditions
- ✅ Performance under load
- ✅ Security validation
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
  "path": "/full/path/to/file",
  "filename": "filename.ext",
  "size": 1024,
  "created": "2025-08-10T12:00:00Z",
  "modified": "2025-08-10T12:00:00Z",
  "accessed": "2025-08-10T12:00:00Z"
}
```

## 🐛 Known Issues & Fixes

- **Issue #14**: Space handling in queries - Fixed in optimized version
- **Empty Query Handling**: Now returns proper error messages
- **Performance**: Improved handling of large result sets

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

- 📖 [Documentation](SEARCH_SYNTAX.md)
- 🐛 [Issue Tracker](https://github.com/Colton-wq/mcp-everything-search-optimized/issues)
- 📧 [Contact](mailto:your-email@example.com)

---

**Note**: This is an optimized version with security and performance improvements. For the original version, see [mamertofabian/mcp-everything-search](https://github.com/mamertofabian/mcp-everything-search).