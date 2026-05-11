#!/usr/bin/env python3
"""
Web Fuzzer for Bug Hunting
Fuzzes a target URL using wordlists and organizes results by response code.
Features:
  - Multi-wordlist support
  - Live console output with colors
  - Organized results directory structure
  - Response code categorization
  - Real-time statistics
"""

import os
import sys
import requests
import threading
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from urllib.parse import urljoin

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class WebFuzzer:
    def __init__(self, base_url, timeout=5):
        """Initialize the fuzzer with base URL and settings."""
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.results_dir = Path('results')
        self.results_dir.mkdir(exist_ok=True)
        
        # Statistics
        self.stats = {
            'total': 0,
            'found': 0,
            'status_codes': defaultdict(int),
            'by_wordlist': defaultdict(lambda: {'found': 0, 'total': 0})
        }
        self.lock = threading.Lock()
        
        # Load wordlists
        self.wordlists = self._load_wordlists()
        
    def _load_wordlists(self):
        """Load all wordlists from ../wordlists directory."""
        wordlist_dir = Path('../wordlists')
        
        if not wordlist_dir.exists():
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} Wordlist directory not found: {wordlist_dir}")
            print(f"Please ensure wordlists are in: {wordlist_dir.absolute()}")
            sys.exit(1)
        
        wordlists = {}
        
        for wordlist_file in wordlist_dir.glob('*'):
            if wordlist_file.is_file():
                try:
                    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                        words = [line.strip() for line in f if line.strip()]
                    wordlists[wordlist_file.name] = words
                    print(f"{Colors.CYAN}[LOADED]{Colors.ENDC} {wordlist_file.name} ({len(words)} entries)")
                except Exception as e:
                    print(f"{Colors.YELLOW}[WARN]{Colors.ENDC} Failed to load {wordlist_file.name}: {e}")
        
        if not wordlists:
            print(f"{Colors.RED}[ERROR]{Colors.ENDC} No wordlists found in {wordlist_dir}")
            sys.exit(1)
        
        return wordlists
    
    def _save_result(self, wordlist_name, status_code, url):
        """Save result to organized directory structure."""
        # Create wordlist-specific directory
        wordlist_dir = self.results_dir / wordlist_name
        wordlist_dir.mkdir(exist_ok=True)
        
        # Create status code file
        status_file = wordlist_dir / f"{status_code}.txt"
        
        with self.lock:
            with open(status_file, 'a', encoding='utf-8') as f:
                f.write(f"{url}\n")
    
    def _print_result(self, wordlist_name, url, status_code, response_time):
        """Print formatted result to console."""
        # Color code based on status
        if 200 <= status_code < 300:
            color = Colors.GREEN
            symbol = "✓"
        elif 300 <= status_code < 400:
            color = Colors.CYAN
            symbol = "→"
        elif 400 <= status_code < 500:
            color = Colors.YELLOW
            symbol = "!"
        else:
            color = Colors.RED
            symbol = "✗"
        
        # Print line with timestamp and timing
        timestamp = datetime.now().strftime("%H:%M:%S")
        output = (f"{Colors.BOLD}[{timestamp}]{Colors.ENDC} "
                 f"{symbol} {color}[{status_code}]{Colors.ENDC} "
                 f"{url:<50} "
                 f"{Colors.BLUE}({response_time:.2f}s){Colors.ENDC} "
                 f"{Colors.YELLOW}[{wordlist_name}]{Colors.ENDC}")
        
        with self.lock:
            print(output)
            self._update_stats(wordlist_name, status_code, 200 <= status_code < 300)
    
    def _update_stats(self, wordlist_name, status_code, is_good):
        """Update statistics."""
        self.stats['total'] += 1
        self.stats['status_codes'][status_code] += 1
        self.stats['by_wordlist'][wordlist_name]['total'] += 1
        
        if is_good:
            self.stats['found'] += 1
            self.stats['by_wordlist'][wordlist_name]['found'] += 1
    
    def _print_stats(self):
        """Print current statistics."""
        good_count = self.stats['found']
        total_count = self.stats['total']
        
        print("\n" + "=" * 100)
        print(f"{Colors.BOLD}{Colors.BLUE}STATISTICS{Colors.ENDC}")
        print("=" * 100)
        print(f"{Colors.GREEN}✓ Good Paths Found: {Colors.BOLD}{good_count}{Colors.ENDC}")
        print(f"{Colors.CYAN}Total Requests: {Colors.BOLD}{total_count}{Colors.ENDC}")
        
        if total_count > 0:
            percentage = (good_count / total_count) * 100
            print(f"Success Rate: {Colors.BOLD}{percentage:.2f}%{Colors.ENDC}\n")
        
        print(f"{Colors.BOLD}Status Code Distribution:{Colors.ENDC}")
        for code in sorted(self.stats['status_codes'].keys()):
            count = self.stats['status_codes'][code]
            percentage = (count / total_count * 100) if total_count > 0 else 0
            print(f"  [{code}] {count:5d} ({percentage:5.2f}%)")
        
        print(f"\n{Colors.BOLD}By Wordlist:{Colors.ENDC}")
        for wl_name, wl_stats in sorted(self.stats['by_wordlist'].items()):
            found = wl_stats['found']
            total = wl_stats['total']
            print(f"  {wl_name:<30} {found:5d}/{total:5d} found")
        
        print("=" * 100 + "\n")
    
    def _make_request(self, wordlist_name, path):
        """Make HTTP request and handle result."""
        url = urljoin(self.base_url + '/', path)
        
        try:
            start_time = datetime.now()
            response = requests.get(url, timeout=self.timeout, verify=False)
            response_time = (datetime.now() - start_time).total_seconds()
            
            status_code = response.status_code
            
            # Save and print results
            self._save_result(wordlist_name, status_code, url)
            self._print_result(wordlist_name, url, status_code, response_time)
            
        except requests.exceptions.Timeout:
            with self.lock:
                print(f"{Colors.RED}[TIMEOUT]{Colors.ENDC} {url}")
        except requests.exceptions.ConnectionError:
            with self.lock:
                print(f"{Colors.RED}[ERROR]{Colors.ENDC} Connection failed: {url}")
        except Exception as e:
            with self.lock:
                print(f"{Colors.RED}[ERROR]{Colors.ENDC} {url} - {str(e)[:50]}")
    
    def fuzz(self, max_workers=10):
        """Start fuzzing with multiple threads."""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        print(f"{Colors.BOLD}{Colors.HEADER}")
        print("╔═══════════════════════════════════════════════════════════════════╗")
        print("║                         WEB FUZZER v1.0                            ║")
        print("║                     Bug Hunting Tool                              ║")
        print("╚═══════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}[CONFIG]{Colors.ENDC}")
        print(f"Target URL: {Colors.CYAN}{self.base_url}{Colors.ENDC}")
        print(f"Wordlists: {Colors.CYAN}{len(self.wordlists)}{Colors.ENDC}")
        print(f"Timeout: {Colors.CYAN}{self.timeout}s{Colors.ENDC}")
        print(f"Workers: {Colors.CYAN}{max_workers}{Colors.ENDC}")
        print(f"Results Dir: {Colors.CYAN}{self.results_dir.absolute()}{Colors.ENDC}\n")
        
        total_paths = sum(len(paths) for paths in self.wordlists.values())
        print(f"{Colors.BOLD}Starting fuzzing ({total_paths} total paths)...{Colors.ENDC}\n")
        
        # Create all tasks
        tasks = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for wordlist_name, paths in self.wordlists.items():
                for path in paths:
                    task = executor.submit(self._make_request, wordlist_name, path)
                    tasks.append(task)
            
            # Wait for completion
            completed = 0
            for future in as_completed(tasks):
                completed += 1
                if completed % 50 == 0:
                    print(f"{Colors.BOLD}{Colors.BLUE}Progress: {completed}/{len(tasks)}{Colors.ENDC}\n")
                try:
                    future.result()
                except Exception as e:
                    print(f"{Colors.RED}[ERROR]{Colors.ENDC} Task failed: {e}")
        
        # Print final statistics
        self._print_stats()
        print(f"{Colors.GREEN}{Colors.BOLD}✓ Fuzzing complete!{Colors.ENDC}")
        print(f"Results saved to: {Colors.CYAN}{self.results_dir.absolute()}{Colors.ENDC}\n")

def main():
    """Main entry point."""
    print()
    
    # Get target URL from user
    target_url = input(f"{Colors.BOLD}Enter target URL{Colors.ENDC} (e.g., http://example.com): ").strip()
    
    if not target_url:
        print(f"{Colors.RED}[ERROR]{Colors.ENDC} URL cannot be empty")
        sys.exit(1)
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url
    
    # Optional: get timeout
    timeout_input = input(f"{Colors.BOLD}Request timeout in seconds{Colors.ENDC} (default 5): ").strip()
    timeout = int(timeout_input) if timeout_input else 5
    
    # Optional: get worker count
    workers_input = input(f"{Colors.BOLD}Number of concurrent workers{Colors.ENDC} (default 10): ").strip()
    max_workers = int(workers_input) if workers_input else 10
    
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # Create and run fuzzer
    fuzzer = WebFuzzer(target_url, timeout=timeout)
    
    try:
        fuzzer.fuzz(max_workers=max_workers)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[INTERRUPTED]{Colors.ENDC} Fuzzing stopped by user")
        fuzzer._print_stats()
        sys.exit(0)

if __name__ == '__main__':
    main()