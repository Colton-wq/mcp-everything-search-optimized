# Everything SDK Setup

This directory should contain the Everything SDK files required for Windows functionality.

## Required Files

### DLL Files (Required for Windows)
Place the following files in the `dll/` subdirectory:

- `Everything64.dll` - 64-bit Everything SDK library
- `Everything32.dll` - 32-bit Everything SDK library (optional)

### Header Files (Optional - for development reference)
Place the following files in the `include/` subdirectory:

- `Everything.h` - C/C++ header file with function declarations
- `Everything.lib` - Import library for linking

## Download Instructions

1. **Download Everything SDK**:
   - Visit: https://www.voidtools.com/support/everything/sdk/
   - Download the latest Everything SDK package
   - Extract the archive

2. **Copy Required Files**:
   ```
   Everything-SDK/
   ├── dll/
   │   ├── Everything64.dll    # Copy from SDK package
   │   └── Everything32.dll    # Copy from SDK package (optional)
   ├── include/
   │   ├── Everything.h        # Copy from SDK package (optional)
   │   └── Everything.lib      # Copy from SDK package (optional)
   └── README.md              # This file
   ```

3. **Verify Installation**:
   - Ensure `Everything64.dll` is present in `Everything-SDK/dll/`
   - The MCP server will automatically detect and use this file

## Environment Variable (Alternative)

Instead of placing files in this directory, you can set the `EVERYTHING_SDK_PATH` environment variable:

```bash
# Windows Command Prompt
set EVERYTHING_SDK_PATH=C:\\path\\to\\Everything64.dll

# Windows PowerShell
$env:EVERYTHING_SDK_PATH = \"C:\\path\\to\\Everything64.dll\"

# Linux/macOS (for cross-platform development)
export EVERYTHING_SDK_PATH=\"/path/to/Everything64.dll\"
```

## Prerequisites

### Windows Requirements
1. **Everything Search Application**:
   - Download and install from: https://www.voidtools.com/
   - Ensure the Everything service is running
   - The application must be running for the SDK to work

2. **System Requirements**:
   - Windows 7 or later
   - Everything 1.4.1 or later
   - Python 3.8 or later

### Verification Steps
1. Install Everything application
2. Start Everything and let it index your drives
3. Place `Everything64.dll` in `Everything-SDK/dll/`
4. Test the MCP server functionality

## Troubleshooting

### Common Issues

1. **\"Failed to load Everything SDK DLL\"**:
   - Verify `Everything64.dll` is in the correct location
   - Check that the Everything application is installed and running
   - Ensure you have the correct architecture (64-bit vs 32-bit)

2. **\"IPC failed (Everything service not running?)\"**:
   - Start the Everything application
   - Ensure the Everything service is running in the background
   - Check Windows Services for \"Everything\" service

3. **\"Invalid call\" or \"Invalid index\" errors**:
   - Update to the latest Everything application version
   - Ensure the SDK DLL matches your Everything version
   - Restart the Everything application

### Debug Mode
Enable debug output by setting the environment variable:
```bash
set EVERYTHING_DEBUG=1
```

## License and Legal

- Everything SDK is provided by voidtools under their license terms
- See: https://www.voidtools.com/License/
- This MCP server is a wrapper around the Everything SDK
- Users must comply with voidtools' license terms when using the SDK

## Support

For Everything SDK specific issues:
- Everything Support: https://www.voidtools.com/support/
- Everything Forum: https://www.voidtools.com/forum/

For MCP server issues:
- GitHub Issues: https://github.com/Colton-wq/mcp-everything-search-optimized/issues