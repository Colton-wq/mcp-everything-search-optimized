"""MCP server implementation for cross-platform file search."""

import json
import platform
import sys
import re
from typing import List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool, Resource, ResourceTemplate, Prompt
from pydantic import BaseModel, Field

from .platform_search import UnifiedSearchQuery, WindowsSpecificParams, build_search_command
from .search_interface import SearchProvider

class SensitiveFileFilter:
    """Filter to prevent access to sensitive files and directories."""
    
    # Sensitive keywords that should be filtered
    SENSITIVE_KEYWORDS = [
        'password', 'passwd', 'pwd', 'secret', 'key', 'token', 'credential',
        'private', 'confidential', 'sensitive', 'security', 'auth', 'login'
    ]
    
    # Sensitive directory patterns (case-insensitive)
    SENSITIVE_PATHS = [
        r'.*[/\\]system32[/\\].*',
        r'.*[/\\]windows[/\\]system.*',
        r'.*[/\\]program files[/\\].*',
        r'.*[/\\]programdata[/\\].*',
        r'.*[/\\]users[/\\][^/\\]+[/\\]appdata[/\\].*',
        r'.*[/\\]\.ssh[/\\].*',
        r'.*[/\\]\.gnupg[/\\].*',
        r'.*[/\\]keychain[/\\].*',
        r'.*[/\\]etc[/\\]shadow.*',
        r'.*[/\\]etc[/\\]passwd.*',
        r'.*[/\\]var[/\\]log[/\\].*',
        r'.*[/\\]registry[/\\].*',
        r'.*[/\\]sam$',
        r'.*[/\\]security$',
        r'.*[/\\]software$',
        r'.*[/\\]system$'
    ]
    
    @classmethod
    def is_sensitive_query(cls, query: str) -> bool:
        """Check if a query contains sensitive keywords."""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in cls.SENSITIVE_KEYWORDS)
    
    @classmethod
    def filter_sensitive_results(cls, results: List, max_filtered: int = 10) -> List:
        """Filter out sensitive files from search results."""
        filtered_results = []
        filtered_count = 0
        
        for result in results:
            if cls._is_sensitive_path(result.path):
                filtered_count += 1
                if filtered_count <= max_filtered:
                    continue  # Skip this result
            filtered_results.append(result)
        
        return filtered_results
    
    @classmethod
    def _is_sensitive_path(cls, path: str) -> bool:
        """Check if a file path is sensitive."""
        path_lower = path.lower()
        
        # Check for sensitive keywords in filename
        if any(keyword in path_lower for keyword in cls.SENSITIVE_KEYWORDS):
            return True
        
        # Check for sensitive directory patterns
        for pattern in cls.SENSITIVE_PATHS:
            if re.match(pattern, path_lower):
                return True
        
        return False

class SearchQuery(BaseModel):
    """Search query parameters."""
    query: str = Field(..., description="Search query string")
    max_results: int = Field(default=100, ge=1, le=1000, description="Maximum number of results")

class WindowsSearchQuery(SearchQuery):
    """Windows-specific search query with Everything SDK parameters."""
    windows_params: WindowsSpecificParams = Field(default_factory=WindowsSpecificParams)

# Global server instance
server = Server("everything-search")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available search tools."""
    return [
        Tool(
            name="search",
            description="Search for files and directories using platform-specific search engines",
            inputSchema={
                "type": "object",
                "properties": {
                    "base": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query string. See platform-specific documentation for syntax details."
                            },
                            "max_results": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 1000,
                                "default": 100,
                                "description": "Maximum number of results to return (1-1000)"
                            }
                        },
                        "required": ["query"]
                    },
                    "windows_params": {
                        "type": "object",
                        "properties": {
                            "match_case": {
                                "type": "boolean",
                                "default": False,
                                "description": "Enable case-sensitive search"
                            },
                            "match_path": {
                                "type": "boolean", 
                                "default": False,
                                "description": "Match against full path instead of filename only"
                            },
                            "match_regex": {
                                "type": "boolean",
                                "default": False,
                                "description": "Enable regex search"
                            },
                            "match_whole_word": {
                                "type": "boolean",
                                "default": False,
                                "description": "Match whole words only"
                            },
                            "sort_by": {
                                "type": "integer",
                                "enum": [1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14],
                                "default": 1,
                                "description": "Sort order for results"
                            }
                        }
                    }
                },
                "required": ["base"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls."""
    if name != "search":
        raise ValueError(f"Unknown tool: {name}")
    
    try:
        # Get current platform
        current_platform = platform.system().lower()
        
        # Extract base parameters
        base_params = arguments.get('base', {})
        if not isinstance(base_params, dict):
            raise ValueError("'base' parameter must be a dictionary")
        
        # Handle windows_params
        windows_params = None
        if 'windows_params' in arguments:
            if isinstance(arguments['windows_params'], str):
                # If it's a string, try to parse as JSON
                try:
                    windows_params = json.loads(arguments['windows_params'])
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON in 'windows_params'")
            elif isinstance(arguments['windows_params'], dict):
                # If already a dict, use directly
                windows_params = arguments['windows_params']
            else:
                raise ValueError("'windows_params' must be a string or dictionary")

        # Combine parameters
        query_params = {
            **base_params,
            'windows_params': windows_params
        }

        # Validate query before processing
        query_string = query_params.get('query', '').strip()
        if not query_string:
            raise ValueError("Empty query not allowed")

        # Check for sensitive queries
        if SensitiveFileFilter.is_sensitive_query(query_string):
            raise ValueError("Query contains restricted keywords")

        # Check for Issue #14: Quoted string queries
        if '"' in query_string:
            raise ValueError("Quoted string queries not supported")

        # Create unified query
        query = UnifiedSearchQuery(**query_params)

        if current_platform == "windows":
            # Use Everything SDK directly
            platform_params = query.windows_params or WindowsSpecificParams()
            search_provider = SearchProvider()
            
            results = search_provider.search_files(
                query=query.query,
                max_results=query.max_results,
                **platform_params.dict()
            )
        else:
            # Use command-line search for other platforms
            command = build_search_command(query)
            search_provider = SearchProvider()
            
            results = search_provider.search_files(
                query=query.query,
                max_results=query.max_results,
                **query.windows_params.dict() if query.windows_params else {}
            )
        
        # Apply sensitive file filtering to all results
        filtered_results = SensitiveFileFilter.filter_sensitive_results(results)

        return [TextContent(
            type="text",
            text="\n".join([
                f"Path: {r.path}\n"
                f"Filename: {r.filename}"
                f"{f' ({r.extension})' if r.extension else ''}\n"
                f"Size: {r.size:,} bytes\n"
                f"Created: {r.created if r.created else 'N/A'}\n"
                f"Modified: {r.modified if r.modified else 'N/A'}\n"
                f"Accessed: {r.accessed if r.accessed else 'N/A'}\n"
                for r in filtered_results
            ])
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Search failed: {str(e)}"
        )]

async def main():
    """Main entry point for the server."""
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

def configure_windows_console():
    """Configure Windows console for UTF-8 output."""
    if platform.system() == "Windows":
        try:
            import codecs
            import locale
            
            # Set console to UTF-8
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
            
            # Set locale
            try:
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            except locale.Error:
                # Fallback to system default
                pass
                
        except Exception:
            # If configuration fails, continue with defaults
            pass

if __name__ == "__main__":
    configure_windows_console()
    
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)