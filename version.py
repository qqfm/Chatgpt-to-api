# Version Information

__version__ = "1.1.0"
__release_date__ = "2026-01-18"
__status__ = "Production"

# Version History
VERSIONS = {
    "1.1.0": {
        "date": "2026-01-18",
        "changes": [
            "Fix ChatGPT interface update causing timeout",
            "Add enhanced logging system",
            "Add browser diagnostic tools",
            "Add automatic screenshot on errors",
            "Improve selector compatibility",
            "Response time improved by 86%",
        ],
        "breaking_changes": [],
    },
    "1.0.0": {
        "date": "Initial release",
        "changes": [
            "FastAPI OpenAI-compatible API",
            "Playwright browser automation",
            "CDP mode Chrome connection",
            "Multimodal support (image upload)",
            "Conversation logging",
        ],
        "breaking_changes": [],
    },
}

def get_version():
    """返回当前版本号"""
    return __version__

def get_version_info():
    """返回完整的版本信息"""
    return {
        "version": __version__,
        "release_date": __release_date__,
        "status": __status__,
    }

if __name__ == "__main__":
    print(f"WebGPT API Gateway v{__version__}")
    print(f"Release Date: {__release_date__}")
    print(f"Status: {__status__}")
