# TermBoard

**A beautiful, interactive terminal dashboard for Python projects, environments, and tasks.**

## The Problem: "Why not just use a script?"

As developers, we often write `Makefile`s or bash scripts (like `test.sh` or `lint.sh`) to manage our project workflows. While scripts work, they have severe limitations:

1. **Context Switching:** You have to remember the exact command or script name, type it out, and watch it vomit hundreds of lines of output into your terminal, erasing your history.
2. **Environment Hell:** Did you remember to activate your virtual environment? Are you using `uv`, `poetry`, or `conda`? Running the wrong script in the wrong environment is a daily frustration.
3. **Discoverability:** New developers joining your project don't know what scripts exist or what they do.

## The Solution: TermBoard

**TermBoard** replaces your scripts with a persistent, interactive Terminal UI (TUI).

- 🧠 **Smart Environment Detection:** TermBoard automatically detects if you are using `uv`, `poetry`, `pipenv`, or a standard `.venv`, and executes your tasks in the correct environment—no manual activation required.
- ⚡ **Asynchronous Streaming:** Tasks run asynchronously in the background. Their output is streamed directly into a beautiful, scrollable Rich Log window without freezing the UI or polluting your terminal history.
- 🛠️ **Fully Customizable:** Define custom tasks in a `termboard.toml` file. Your team can clone the repo, run `termboard`, and instantly have a UI with clickable buttons for deploying, testing, and building.

## 💖 Support & Community

If you like TermBoard, please consider supporting the project!

- ⭐️ **Star on GitHub**: [HeyShinde/TermBoard](https://github.com/HeyShinde/TermBoard)
- 🐞 **Report Issues**: [GitHub Issues](https://github.com/HeyShinde/TermBoard/issues)
- 💬 **Follow / Contact**: [@heyshinde](https://github.com/HeyShinde)
- 💖 **Sponsor / Donate**: Press the `s` hotkey directly in the TUI, or visit my [GitHub Sponsors](https://github.com/sponsors/HeyShinde) or [Razorpay](https://razorpay.me/@heyshinde).
