#!/usr/bin/env python3
"""
Extract Rust code from LLM response.
This script finds Rust code blocks in the LLM output and extracts clean Rust code.
"""

import sys
import re

def extract_rust_code(input_text):
    """Extract Rust code from markdown code blocks."""
    
    # Look for ```rust or ``` code blocks
    rust_patterns = [
        r'```rust\s*\n(.*?)\n```',  # ```rust ... ```
        r'```\s*\n(.*?)\n```',      # ``` ... ``` (fallback)
    ]
    
    for pattern in rust_patterns:
        matches = re.findall(pattern, input_text, re.DOTALL)
        if matches:
            # Take the first match and clean it up
            code = matches[0].strip()
            
            # Remove any remaining markdown artifacts
            code = re.sub(r'^```.*$', '', code, flags=re.MULTILINE)
            code = re.sub(r'```$', '', code, flags=re.MULTILINE)
            
            # Remove empty lines at start/end
            code = code.strip()
            
            if code:
                return code
    
    # If no code blocks found, try to extract any Rust-like code
    lines = input_text.split('\n')
    rust_lines = []
    in_code = False
    
    for line in lines:
        # Look for Rust keywords or patterns
        if any(keyword in line for keyword in ['fn ', 'use ', 'mod ', 'pub ', 'struct ', 'enum ', 'impl ', 'let ', 'println!', 'use std::']):
            in_code = True
        
        if in_code:
            # Stop if we hit markdown or non-Rust content
            if line.strip().startswith('```') or line.strip().startswith('#') or line.strip().startswith('*'):
                break
            rust_lines.append(line)
    
    if rust_lines:
        return '\n'.join(rust_lines).strip()
    
    # If nothing found, return a minimal Rust program
    if any(keyword in input_text for keyword in ['fn ', 'use ', 'mod ', 'pub ', 'struct ', 'enum ', 'impl ']):
        return input_text.strip()
    
    # If nothing found, return a minimal Rust program
    return '''fn main() {
    println!("Hello, world!");
}'''

def main():
    """Main function to extract Rust code from stdin."""
    try:
        # Read input from stdin
        input_text = sys.stdin.read()
        
        # Extract Rust code
        rust_code = extract_rust_code(input_text)
        
        # Output to stdout
        print(rust_code)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        # Return minimal Rust program on error
        print('''fn main() {
    println!("Hello, world!");
}''')
        sys.exit(1)

if __name__ == "__main__":
    main()
