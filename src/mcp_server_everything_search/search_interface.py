"""Platform-agnostic search interface for MCP."""

import abc
import platform
import subprocess
import os
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SearchResult:
    """Universal search result structure."""
    path: str
    filename: str
    extension: Optional[str] = None
    size: Optional[int] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    accessed: Optional[datetime] = None
    attributes: Optional[str] = None

class SearchProvider:
    """Concrete search provider that handles all platforms."""
    
    def search_files(
        self,
        query: str,
        max_results: int = 100,
        match_path: bool = False,
        match_case: bool = False,
        match_whole_word: bool = False,
        match_regex: bool = False,
        sort_by: Optional[int] = None
    ) -> List[SearchResult]:
        """Execute a file search using platform-specific methods."""
        system = platform.system().lower()
        if system == 'darwin':
            return self._search_macos(query, max_results, match_path, match_case, match_whole_word, match_regex, sort_by)
        elif system == 'linux':
            return self._search_linux(query, max_results, match_path, match_case, match_whole_word, match_regex, sort_by)
        elif system == 'windows':
            return self._search_windows(query, max_results, match_path, match_case, match_whole_word, match_regex, sort_by)
        else:
            raise NotImplementedError(f"No search provider available for {system}")

    def _convert_path_to_result(self, path: str) -> SearchResult:
        """Convert a path to a SearchResult with file information."""
        try:
            path_obj = Path(path)
            stat = path_obj.stat()
            return SearchResult(
                path=str(path_obj),
                filename=path_obj.name,
                extension=path_obj.suffix[1:] if path_obj.suffix else None,
                size=stat.st_size,
                created=datetime.fromtimestamp(stat.st_ctime),
                modified=datetime.fromtimestamp(stat.st_mtime),
                accessed=datetime.fromtimestamp(stat.st_atime)
            )
        except (OSError, ValueError) as e:
            # If we can't access the file, return basic info
            return SearchResult(
                path=str(path),
                filename=os.path.basename(path)
            )

    def _search_macos(
        self,
        query: str,
        max_results: int = 100,
        match_path: bool = False,
        match_case: bool = False,
        match_whole_word: bool = False,
        match_regex: bool = False,
        sort_by: Optional[int] = None
    ) -> List[SearchResult]:
        """macOS search implementation using mdfind."""
        try:
            # Build mdfind command
            cmd = ['mdfind']
            if match_path:
                # When matching path, don't use -name
                cmd.append(query)
            else:
                cmd.extend(['-name', query])
            
            # Execute search
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"mdfind failed: {result.stderr}")

            # Process results
            paths = result.stdout.splitlines()[:max_results]
            return [self._convert_path_to_result(path) for path in paths]
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Search failed: {e}")

    def _search_linux(
        self,
        query: str,
        max_results: int = 100,
        match_path: bool = False,
        match_case: bool = False,
        match_whole_word: bool = False,
        match_regex: bool = False,
        sort_by: Optional[int] = None
    ) -> List[SearchResult]:
        """Linux search implementation using locate/plocate."""
        # Check for available locate command
        locate_cmd = None
        locate_type = None

        # Check for plocate first (newer version)
        plocate_check = subprocess.run(['which', 'plocate'], capture_output=True)
        if plocate_check.returncode == 0:
            locate_cmd = 'plocate'
            locate_type = 'plocate'
        else:
            # Check for mlocate
            mlocate_check = subprocess.run(['which', 'locate'], capture_output=True)
            if mlocate_check.returncode == 0:
                locate_cmd = 'locate'
                locate_type = 'mlocate'
            else:
                raise RuntimeError(
                    "Neither 'locate' nor 'plocate' is installed. Please install one:\n"
                    "Ubuntu/Debian: sudo apt-get install plocate\n"
                    "              or\n"
                    "              sudo apt-get install mlocate\n"
                    "Fedora: sudo dnf install mlocate\n"
                    "After installation, the database will be updated automatically, or run:\n"
                    "For plocate: sudo updatedb\n"
                    "For mlocate: sudo /etc/cron.daily/mlocate"
                )

        try:
            # Build locate command
            cmd = [locate_cmd]
            if not match_case:
                cmd.append('-i')
            if match_regex:
                cmd.append('--regex' if locate_type == 'mlocate' else '-r')
            cmd.append(query)
            
            # Execute search
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                error_msg = result.stderr.lower()
                if "no such file or directory" in error_msg or "database" in error_msg:
                    raise RuntimeError(
                        f"The {locate_type} database needs to be created. "
                        f"Please run: sudo updatedb"
                    )
                raise RuntimeError(f"{locate_cmd} failed: {result.stderr}")

            # Process results
            paths = result.stdout.splitlines()[:max_results]
            return [self._convert_path_to_result(path) for path in paths]
            
        except FileNotFoundError:
            raise RuntimeError(
                f"The {locate_cmd} command disappeared. Please reinstall:\n"
                "Ubuntu/Debian: sudo apt-get install plocate\n"
                "              or\n"
                "              sudo apt-get install mlocate\n"
                "Fedora: sudo dnf install mlocate"
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Search failed: {e}")

    def _search_windows(
        self,
        query: str,
        max_results: int = 100,
        match_path: bool = False,
        match_case: bool = False,
        match_whole_word: bool = False,
        match_regex: bool = False,
        sort_by: Optional[int] = None
    ) -> List[SearchResult]:
        """Windows search implementation using Everything SDK."""
        import os
        from .everything_sdk import EverythingSDK

        # Use relative path from current file directory as default
        current_dir = os.path.dirname(os.path.abspath(__file__))
        default_dll_path = os.path.join(current_dir, '..', '..', 'Everything-SDK', 'dll', 'Everything64.dll')
        default_dll_path = os.path.normpath(default_dll_path)

        dll_path = os.getenv('EVERYTHING_SDK_PATH', default_dll_path)
        everything_sdk = EverythingSDK(dll_path)

        # Replace double backslashes with single backslashes
        query = query.replace("\\\\", "\\")
        # If the query contains forward slashes, replace them with backslashes
        query = query.replace("/", "\\")

        return everything_sdk.search_files(
            query=query,
            max_results=max_results,
            match_path=match_path,
            match_case=match_case,
            match_whole_word=match_whole_word,
            match_regex=match_regex,
            sort_by=sort_by
        )