#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Keyword-Based Search with BM25 Algorithm
Searches patterns and tasks by extracting keywords from user prompts
"""

import json
import re
from pathlib import Path
from math import log
from collections import Counter, defaultdict

DATA_DIR = Path(__file__).parent / "data"


class KeywordSearch:
    def __init__(self):
        self.index = []
        self.doc_count = 0
        self.avg_doc_length = 0
        self.term_doc_freq = defaultdict(int)  # How many docs contain term
        self._build_index()
    
    def _build_index(self):
        """Build search index from all patterns and tasks JSON files.
        Walk directories using os.walk with followlinks=True so symlinked/junction
        directories are traversed correctly (Windows junctions, Unix symlinks).
        """
        import os

        all_files = []
        for sub in ("patterns", "tasks"):
            dirp = DATA_DIR / sub
            if not dirp.exists():
                continue

            # Use os.walk to follow symlinks reliably
            for root, dirs, files in os.walk(dirp, followlinks=True):
                for fname in files:
                    if fname.lower().endswith('.json'):
                        all_files.append(Path(root) / fname)
        
        total_length = 0
        
        for json_file in all_files:
            # open files even if they live outside DATA_DIR (symlink targets)
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract searchable text
                searchable = self._extract_searchable_text(data)
                tokens = self._tokenize(searchable)

                # Compute file path relative to DATA_DIR if possible. Handle symlink targets outside DATA_DIR.
                try:
                    file_path_rel = str(json_file.relative_to(DATA_DIR))
                except Exception:
                    file_path_rel = str(json_file)

                # Determine file type by checking if path contains the tasks directory
                file_type_var = 'task' if str(DATA_DIR / 'tasks') in str(json_file) else 'pattern'

                doc = {
                    'id': data.get('id', ''),
                    'name': data.get('name', ''),
                    'description': data.get('description', ''),
                    'keywords': data.get('keywords', []),
                    'complexity': data.get('complexity', ''),
                    'file_path': file_path_rel,
                    'file_type': file_type_var,
                    'data': data,
                    'tokens': tokens,
                    'doc_length': len(tokens)
                }
                
                self.index.append(doc)
                total_length += len(tokens)
                
                # Track term document frequency
                for term in set(tokens):
                    self.term_doc_freq[term] += 1
        
        self.doc_count = len(self.index)
        self.avg_doc_length = total_length / self.doc_count if self.doc_count > 0 else 0
    
    def _extract_searchable_text(self, data):
        """Extract all searchable text from document"""
        text_parts = [
            data.get('id', ''),
            data.get('name', ''),
            data.get('description', ''),
        ]
        
        # Add keywords (with higher weight by repeating)
        keywords = data.get('keywords', [])
        if keywords:
            text_parts.extend(keywords * 3)  # Keywords get 3x weight
        
        return ' '.join(str(part) for part in text_parts)
    
    def _tokenize(self, text):
        """Convert text to tokens"""
        # Lowercase and extract words
        tokens = re.findall(r'\w+', text.lower())
        return tokens
    
    def extract_keywords_from_query(self, query):
        """
        Extract meaningful keywords from user query
        Examples:
        - "create api /api/products/search" -> ["create", "api", "products", "search", "rest", "endpoint"]
        - "add JWT authentication" -> ["add", "jwt", "authentication", "security", "token"]
        """
        keywords = []
        query_lower = query.lower()
        
        # Extract HTTP methods
        http_methods = re.findall(r'\b(get|post|put|delete|patch)\b', query_lower)
        keywords.extend(http_methods)
        
        # Extract entity names from /api/entity pattern
        entity_match = re.search(r'/api/(\w+)', query_lower)
        if entity_match:
            keywords.append(entity_match.group(1))
        
        # Technical keyword mappings
        keyword_mappings = {
            'crud': ['crud', 'create.*api', 'full.*endpoint', 'rest.*api'],
            'authentication': ['auth', 'jwt', 'login', 'secure', 'token', 'protect'],
            'repository': ['repository', 'database', 'dao', 'data.*access', 'jpa'],
            'service': ['service', 'business.*logic', 'service.*layer'],
            'controller': ['controller', 'endpoint', 'rest', 'api', 'mapping'],
            'pagination': ['pagina', 'page', 'sort', 'limit', 'offset'],
            'validation': ['validat', 'constraint', 'check'],
            'search': ['search', 'filter', 'query', 'find'],
            'configuration': ['config', 'application.yaml', 'properties', 'setup'],
            'logging': ['log', 'logging', 'logback', 'slf4j'],
            'security': ['security', 'secure', 'protect', 'spring.*security'],
            'test': ['test', 'unit.*test', 'integration.*test', 'mock']
        }
        
        for keyword, patterns in keyword_mappings.items():
            if any(re.search(pattern, query_lower) for pattern in patterns):
                keywords.append(keyword)
        
        # Add all significant words from query
        words = self._tokenize(query)
        stopwords = {'the', 'a', 'an', 'to', 'for', 'with', 'in', 'on', 'me', 'help', 'please', 'want', 'need', 'how', 'can', 'i'}
        keywords.extend([w for w in words if w not in stopwords])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)
        
        return unique_keywords
    
    def search_bm25(self, query, top_k=5, k1=1.5, b=0.75):
        """
        BM25 ranking algorithm
        
        Parameters:
        - query: User search query
        - top_k: Number of results to return
        - k1: Term frequency saturation parameter (1.2-2.0)
        - b: Length normalization parameter (0.75 is standard)
        
        Returns: List of top matching documents with scores
        """
        query_keywords = self.extract_keywords_from_query(query)
        query_tokens = self._tokenize(' '.join(query_keywords))
        if not query_tokens:
            return []
        
        scores = []
        
        for doc in self.index:
            score = self._calculate_bm25_score(
                query_tokens, 
                doc['tokens'], 
                doc['doc_length'],
                k1, 
                b
            )
            
            if score > 0:
                scores.append({
                    'id': doc['id'],
                    'name': doc['name'],
                    'description': doc['description'],
                    'keywords': doc['keywords'],
                    'complexity': doc['complexity'],
                    'file_path': doc['file_path'],
                    'file_type': doc['file_type'],
                    'score': score,
                    'data': doc['data']
                })
        
        # Sort by score descending
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        return scores[:top_k]
    
    def _calculate_bm25_score(self, query_tokens, doc_tokens, doc_length, k1, b):
        """Calculate BM25 score for a document"""
        score = 0.0
        doc_term_freq = Counter(doc_tokens)
        
        for term in set(query_tokens):
            if term not in doc_term_freq:
                continue
            
            # Term frequency in document
            tf = doc_term_freq[term]
            
            # Document frequency (how many docs contain this term)
            df = self.term_doc_freq.get(term, 0)
            
            if df == 0:
                continue
            
            # IDF component (inverse document frequency)
            idf = log((self.doc_count - df + 0.5) / (df + 0.5) + 1.0)
            
            # Length normalization
            length_norm = 1 - b + b * (doc_length / self.avg_doc_length)
            
            # BM25 formula
            term_score = idf * (tf * (k1 + 1)) / (tf + k1 * length_norm)
            score += term_score
        
        return score
    
    def format_results(self, results, query):
        """Format search results with enhanced display"""
    
        if not results:
            return self.format_no_results(query)
        
        # Calculate metadata
        top_score = results[0]['score']
        quality = self.get_quality_level(top_score)
        
        output = []
        
        # Header
        output.append("=" * 70)
        output.append(f"🔍 SEARCH RESULTS FOR: \"{query}\"")
        output.append("=" * 70)
        output.append(f"\n📊 Found: {len(results)} matches | Top Score: {top_score:.2f}/10 | Quality: {quality}\n")
        
        # Results
        for i, result in enumerate(results, 1):
            output.append(self.format_single_result(result, i, is_top=(i==1)))
        
        # Recommendation
        output.append("\n" + "=" * 70)
        output.append("💡 AGENT RECOMMENDATION")
        output.append("=" * 70)
        output.append(self.format_recommendation(results[0], quality))
        
        return "\n".join(output)


    def get_quality_level(self, score):
        """Determine quality level from score"""
        if score >= 8.0:
            return "EXCELLENT ⭐⭐⭐⭐⭐"
        elif score >= 6.0:
            return "GOOD ⭐⭐⭐⭐"
        elif score >= 4.0:
            return "MODERATE ⭐⭐⭐"
        elif score >= 2.0:
            return "WEAK ⭐⭐"
        else:
            return "NOT RELEVANT ⭐"


    def format_single_result(self, result, rank, is_top=False):
        """Format a single search result"""
        
        emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
        recommended = " [RECOMMENDED]" if is_top and result['score'] >= 8.0 else ""
        
        lines = [
            "-" * 70,
            f"{emoji}{recommended} {result['name']}",
            "-" * 70,
            f"ID:          {result['id']}",
            f"Type:        {result['file_type']}",
            f"Score:       {result['score']:.2f}/10 {self.get_stars(result['score'])}",
            f"File:        {result['file_path']}",
            f"Match:       {self.get_quality_level(result['score']).split()[0]}",
            f"\nDescription:",
            result['description'],
        ]
        
        return "\n".join(lines)


    def get_stars(self, score):
        """Convert score to star rating"""
        stars = int(score / 2)  # 0-10 -> 0-5 stars
        return "⭐" * stars


    def format_recommendation(self, top_result, quality):
        """Format agent recommendation section"""
        
        if top_result['score'] >= 8.0:
            action = f"Use: #{1} ({top_result['id']}) - {quality.split()[0]} match"
            reason = f"""
    Reason:
    - Score is {top_result['score']:.2f}/10 (excellent quality)
    - Provides complete solution
    - Matches user intent perfectly

    Next step:
    → Ask user: "Should I proceed with '{top_result['name']}' {top_result['file_type']}?"
    """
        elif top_result['score'] >= 6.0:
            action = f"Consider: #{1} ({top_result['id']}) - {quality.split()[0]} match"
            reason = f"""
    Reason:
    - Score is {top_result['score']:.2f}/10 (good quality)
    - May need minor adjustments

    Next step:
    → Show top 2-3 options and ask user to choose
    """
        else:
            action = f"⚠️  Low quality match - Score: {top_result['score']:.2f}/10"
            reason = """
    Recommendation:
    - Consider trying different search keywords
    - Or offer to create custom implementation

    Next step:
    → Ask user if they want to: (1) Try new search, (2) Proceed anyway, (3) Custom code
    """
        
        return f"{action}\n{reason}"


    def format_no_results(self, query):
        """Format output when no results found"""
        
        return f"""
    {"=" * 70}
    🔍 SEARCH RESULTS FOR: "{query}"
    {"=" * 70}

    ❌ No matching patterns or tasks found.

    💡 SUGGESTIONS:

    1. Try different keywords:
    • Broader terms: "api", "crud", "controller"
    • Specific features: "list", "get all", "pagination"

    2. Common searches that might help:
    • python .coding-agent/search_engine.py "create rest api"
    • python .coding-agent/search_engine.py "controller service repository"

    3. Ask agent to create custom implementation

    {"=" * 70}
    """

    # def format_results(self, results, mode='summary'):
    #     """Format search results for display"""
    #     if not results:
    #         return "No results found."
        
    #     output = ["# Search Results\n"]
        
    #     for i, result in enumerate(results, 1):
    #         output.append(f"## {i}. {result['name']}")
    #         output.append(f"**ID:** {result['id']}")
    #         output.append(f"**Type:** {result['file_type']}")
    #         output.append(f"**Score:** {result['score']:.2f}")
    #         output.append(f"**File:** {result['file_path']}")
            
    #         # if result['keywords']:
    #         #     output.append(f"**Keywords:** {', '.join(result['keywords'])}")
            
    #         output.append(f"\n{result['description']}\n")
            
    #         if mode == 'full':
    #             # Show steps if available
    #             steps = result['data'].get('steps', [])
    #             tasks = result['data'].get('tasks', [])
                
    #             if steps:
    #                 output.append("**Steps:**")
    #                 for step in steps:
    #                     output.append(f"  - {step.get('title', 'N/A')}")
    #                 output.append("")
                
    #             if tasks:
    #                 output.append("**Workflow:**")
    #                 for task in tasks:
    #                     output.append(f"  {task.get('step', '')}. {task.get('name', 'N/A')}")
    #                 output.append("")
        
    #     return '\n'.join(output)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Keyword-Based Pattern/Task Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top", type=int, default=5, help="Number of results (default: 5)")
    # parser.add_argument("--mode", choices=['summary', 'full'], default='summary', 
    #                    help="Output mode")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--show-keywords", action="store_true", 
                       help="Show extracted keywords from query")
    
    args = parser.parse_args()
    
    # Initialize search
    searcher = KeywordSearch()
    
    # Show extracted keywords if requested
    if args.show_keywords:
        keywords = searcher.extract_keywords_from_query(args.query)
        print(f"Extracted keywords: {keywords}\n")
    
    # Search
    results = searcher.search_bm25(args.query, top_k=args.top)
    
    # Output
    if args.json:
        # Remove 'data' field for cleaner JSON output
        clean_results = [{k: v for k, v in r.items() if k != 'data'} for r in results]
        print(json.dumps(clean_results, indent=2))
    else:
        print(searcher.format_results(results, args.query))
