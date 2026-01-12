#!/usr/bin/env python3
"""
Project initialization logic for Coding Agent
Creates .coding-agent folder with patterns, tasks, and search engine
Places AI-specific prompt files in provider-specific locations
"""

import json
import shutil
import sys
from pathlib import Path


def init_project(provider):
    """
    Initialize coding-agent in the current project
    
    Args:
        provider: AI provider (claude, copilot)
    """
    cwd = Path.cwd()
    
    # Create .coding-agent directory
    coding_agent_dir = cwd / ".coding-agent"
    
    if coding_agent_dir.exists():
        print(f"❌ Error: {coding_agent_dir} already exists!")
        print(f"   If you want to reinitialize, delete it first: rm -rf {coding_agent_dir}")
        sys.exit(1)
    
    # Check if AI provider-specific prompt already exists
    provider_paths = {
        'copilot': cwd / ".github" / "prompts " / "coding-agent.prompt.md",
        'claude': cwd / ".claude" / "skills" / "coding-agent" / "SKILL.md",
    }
    
    provider_prompt_path = provider_paths.get(provider)
    if provider_prompt_path and provider_prompt_path.exists():
        print(f"❌ Error: {provider_prompt_path} already exists!")
        print(f"   If you want to reinitialize, delete it first: rm {provider_prompt_path}")
        sys.exit(1)
    
    print(f"✨ Initializing Coding Agent with {provider.upper()}...")
    print(f"📁 Creating .coding-agent directory...")
    
    coding_agent_dir.mkdir(parents=True, exist_ok=True)
    
    coding_agent_dir.mkdir(parents=True, exist_ok=True)
    
    # Resolve library root directory (package contains data/code folders now)
    package_dir = Path(__file__).parent  # coding_agent package directory
    lib_root = package_dir  # Data is now inside the package
    lib_data = lib_root / "data"
    lib_code = lib_root / "code"
    
    # Verify data directory exists
    if not lib_data.exists():
        print(f"❌ Error: Could not find data directory at {lib_data}")
        print(f"\n💡 This usually means the package wasn't installed correctly.")
        print(f"   Try reinstalling: pip install --force-reinstall coding-agent")
        sys.exit(1)

    lib_data = lib_root / "data"
    lib_code = lib_root / "code"

    # 1. Create config.json
    print("📝 Creating config.json...")
    config = {
        "ai_provider": provider,
        "version": "0.1.0",
        "patterns_path": "patterns",
        "tasks_path": "tasks",
        "code_path": "code",
        "search_engine": "search_engine.py"
    }

    with open(coding_agent_dir / "config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)

    # 2. Create symlinks or copy directories
    print("🔗 Setting up pattern/task libraries...")

    # Symlink patterns
    patterns_src = lib_data / "patterns"
    patterns_dst = coding_agent_dir / "data" / "patterns"
    if patterns_src.exists():
        try:
            if sys.platform == "win32":
                # Windows: use directory junction
                import subprocess
                subprocess.run(["mklink", "/J", str(patterns_dst), str(patterns_src)], 
                             check=True, capture_output=True, shell=True)
            else:
                # Unix: use symlink
                patterns_dst.symlink_to(patterns_src)
        except Exception as e:
            print(f"⚠️  Could not create symlink for patterns: {e}")
            print("   Copying patterns instead...")
            shutil.copytree(patterns_src, patterns_dst)

    # Symlink tasks
    tasks_src = lib_data / "tasks"
    tasks_dst = coding_agent_dir / "data" / "tasks"
    if tasks_src.exists():
        try:
            if sys.platform == "win32":
                import subprocess
                subprocess.run(["mklink", "/J", str(tasks_dst), str(tasks_src)], 
                             check=True, capture_output=True, shell=True)
            else:
                tasks_dst.symlink_to(tasks_src)
        except Exception as e:
            print(f"⚠️  Could not create symlink for tasks: {e}")
            print("   Copying tasks instead...")
            shutil.copytree(tasks_src, tasks_dst)

    # Symlink code examples
    if lib_code.exists():
        code_dst = coding_agent_dir / "code"
        try:
            if sys.platform == "win32":
                import subprocess
                subprocess.run(["mklink", "/J", str(code_dst), str(lib_code)], 
                             check=True, capture_output=True, shell=True)
            else:
                code_dst.symlink_to(lib_code)
        except Exception as e:
            print(f"⚠️  Could not create symlink for code: {e}")
            print("   Copying code instead...")
            shutil.copytree(lib_code, code_dst)

    # 3. Copy search engine
    print("🔍 Setting up search engine...")
    search_src = package_dir / "search_engine.py"
    search_dst = coding_agent_dir / "search_engine.py"

    if search_src.exists():
        shutil.copy2(search_src, search_dst)
    else:
        print(f"⚠️  Warning: Could not find search_engine.py at {search_src}")
    
    # 4. Create provider-specific system prompt
    print(f"🤖 Creating {provider.upper()} system prompt...")
    system_prompt = _generate_system_prompt(provider)
    
    # Place prompt in provider-specific location
    if provider == 'copilot':
        # GitHub Copilot: .github/prompts/coding-agent.prompt.md
        prompt_dir = cwd / ".github" / "prompts"
        prompt_dir.mkdir(parents=True, exist_ok=True)
        prompt_file = prompt_dir / "coding-agent.prompt.md"
        prompt_dir = cwd / ".github" / "instructions"
        prompt_dir.mkdir(parents=True, exist_ok=True)
        instruction_file = prompt_dir / "coding-agent.instructions.md"
        prompt_files = [prompt_file, instruction_file]
        for prompt_file in prompt_files:
            print(f"   → {prompt_file.relative_to(cwd)}")
    elif provider == 'claude':
        # Claude: .claude/skills/coding-agent/SKILL.md
        prompt_dir = cwd / ".claude" / "skills" / "coding-agent"
        prompt_dir.mkdir(parents=True, exist_ok=True)
        prompt_files = [prompt_dir / "SKILL.md"]
        for prompt_file in prompt_files:
            print(f"   → {prompt_file.relative_to(cwd)}")
    else:
        raise ValueError(f"Unsupported provider: {provider}")
    
    for prompt_file in prompt_files:
        if prompt_file.exists():
            prompt_file.unlink()
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(system_prompt)
    
    # 5. Create README in .coding-agent
    print("📖 Creating README...")
    readme = _generate_readme(provider)
    
    with open(coding_agent_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
    
    # 6. Update .gitignore
    print("🔒 Updating .gitignore...")
    gitignore_path = cwd / ".gitignore"
    
    # Entries to add
    gitignore_entries = [".coding-agent/\n"]
    
    # Don't add provider folders to gitignore - they should be committed!
    # The prompts are part of the project setup
    
    if gitignore_path.exists():
        # Read existing content
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()
        
        # Only add if not already present
        entries_to_add = [entry for entry in gitignore_entries if entry.strip() not in existing_content]
        
        if entries_to_add:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                if not existing_content.endswith('\n'):
                    f.write('\n')
                f.write(''.join(entries_to_add))
    else:
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(''.join(gitignore_entries))
    
    print("\n✅ Coding Agent initialized successfully!")
    print(f"\n📍 Data Location: {coding_agent_dir.relative_to(cwd)}")
    print(f"📍 Prompt Location: {prompt_file.relative_to(cwd)}")
    print(f"\n📚 Available Resources:")
    print(f"   - Patterns: {coding_agent_dir.relative_to(cwd)}/patterns/")
    print(f"   - Tasks: {coding_agent_dir.relative_to(cwd)}/tasks/")
    print(f"   - Code Examples: {coding_agent_dir.relative_to(cwd)}/code/")
    print(f"   - Search Tool: {coding_agent_dir.relative_to(cwd)}/search_engine.py")
    
    if provider == 'copilot':
        print(f"\n💡 GitHub Copilot will automatically discover your prompt at:")
        print(f"   {prompt_file.relative_to(cwd)}")
        print(f"\n   Start coding and Copilot will use these patterns!")
    elif provider == 'claude':
        print(f"\n💡 Claude Projects will automatically discover your skill at:")
        print(f"   {prompt_file.relative_to(cwd)}")
        print(f"\n   Open your project in Claude and ask for help!")
    else:
        print(f"\n💡 Next steps:")
        print(f"   - View the prompt: cat {prompt_file.relative_to(cwd)}")
        print(f"   - Copy it to your AI assistant")
        print(f"   - Start building!")


def _generate_system_prompt(provider):
    """Generate AI provider-specific system prompt"""
    with open(Path(__file__).parent / "templates/prompt.template.md", 'r', encoding='utf-8') as f:
        template = f.read()
    return template.replace("{{AI_PROVIDER}}", provider.capitalize())


def _generate_readme(provider):
    """Generate quick reference README"""
    
    with open(Path(__file__).parent / "templates/README.template.md", 'r', encoding='utf-8') as f:
        template = f.read()
    return template.replace("{{AI_PROVIDER}}", provider.capitalize())


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: init.py <provider>")
        sys.exit(1)
    
    provider = sys.argv[1]
    init_project(provider)

