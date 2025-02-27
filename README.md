# LogKeeper - Python Logger with Custom Issue Registry

**Looking for a robust, fully customizable logging solution that goes beyond Python’s built-in logging basics?**  
Meet **Project Logkeeper**: a clean, scalable logger setup that empowers you to **manage custom exceptions**, **attach contextual codes** to your logs, and **adapt** seamlessly to any size of application.

---

## Why Choose Project Logger?

1. **Enhanced Clarity & Structure**  
   - **Issue Registry**: Easily register and retrieve custom exceptions (warnings, errors, “debuggers”) with a single, centralized pattern.  
   - **Logger Adapter**: Provides a flexible way to insert extra fields (like issue codes) and ensures consistent logs across your system.

2. **No More Spaghetti Imports**  
   - Automatic loading of “custom issues” ensures they’re registered without repeated code.  
   - Decorator-based registration means you can add new issues in just one line—no messing with manual dictionary lookups.

3. **Easy Debugging & Observability**  
   - **Structured logs**: Attach meaningful codes (`I1001`, `D2002`, etc.) to your INFO/DEBUG messages, so you can rapidly filter logs in your monitoring tools.  
   - Built-in support for advanced logging formats (via YAML config), making it simple to adopt JSON or other structured outputs.

4. **Cleanly Adheres to SOLID Principles**  
   - **Single Responsibility**: `factory.py` sets up logging, `registry.py` handles custom issues, `adapter.py` modifies log behavior.  
   - **Open/Closed for Extension**: Add or remove issues, change logging output, or create specialized adapters — no major refactoring needed.

5. **Production-Ready**  
   - Built for **scalability**: If you’re running a microservice architecture or a large monolith, Project LogKeeper can adapt.  
   - Suitable for **enterprise** dev teams who need better tracking, debugging, and error classification at scale.

---

## How It Works

1. **Issue Registry**  
   - A single class (`registry.py`) that stores references to your custom exceptions and warnings.  
   - Extend it by adding decorated classes in `custom.py` — they’re automatically registered and discoverable anywhere in your code.

2. **Logger Factory**  
   - `factory.py` uses lazy loading to set up logging **only once**, reading from a YAML config (`config.yaml`).  
   - Returns either a **basic Logger** or a **custom LoggerAdapter** (in `adapter.py`) that automatically includes codes, advanced context, etc.

3. **Custom Issues**  
   - In `logs/issues/custom.py`, create your own `class MyCustomError(Exception): ...` and decorate it. Done — no extra lines needed to register.  
   - Retrieve these issues using `registry.get("MyCustomError")` or direct usage in your code.

4. **Configurable Output**  
   - `settings/config.yaml` can define custom handlers, formatters (e.g., JSON logs), or advanced rotation policies.  
   - Fall back to a default configuration if the YAML is not found, so it *just works* out of the box.

---

## Quickstart Guide

1. **Clone the Repo**  
   ```bash
   git clone https://github.com/hassanmoin980/python-logkeeper.git
   cd python-logkeeper
   ```

2. **Install Requirements**  
   ```bash
   pip install -r ./logs/requirements.txt
   ```

3. **Explore the Code**  
   - `logs/core/factory.py`: The logging setup (create and configure loggers).  
   - `logs/core/registry.py`: The single source of truth for custom errors/warnings.  
   - `logs/core/adapter.py`: A handy LoggerAdapter if you want to automatically add codes or context.  
   - `logs/issues/custom.py`: A sample place to declare your custom issues.

4. **Run**  
   ```bash
   python test.py
   ```
   or 
   ```bash
   python logs/core/factory.py
   ```
   Depending on how your code is structured, you’ll see the logger in action!

5. **Add Your Own Issues**  
   Just open `custom.py`, decorate your exception or warning class:

   ```python
   from logs.core.registry import register

   @register("MyExclusiveError", code="E1001")
   class MyExclusiveError(Exception):
       pass
   ```

   Next time you run, `MyExclusiveError` is available for logging or raising, automatically.

---

## Why It’s Better Than Basic Logging

- **Basic Python logging** can get messy if you have multiple modules, custom error classes, or you need consistent formatting in large teams.  
- **Project LogKeeper** centralizes these concerns with a *factory*, a *registry*, and *adapters*, giving you a one-stop solution that scales as your codebase grows.  
- Decorators eliminate boilerplate—no more repetitive “dictionary insert” for each new custom class.

---

## Contribute & Share

- **Star** this repository if it helps you!  
- [Open an issue](https://github.com/hassanmoin980/python-logkeeper/issues) or submit a pull request for suggestions or features.  
- Spread the word to your fellow developers so they can also benefit from a clean, professional logging framework in Python.

Take the **chaos** out of debugging—start using **Python LogKeeper** today. Your future self (and your team) will thank you!