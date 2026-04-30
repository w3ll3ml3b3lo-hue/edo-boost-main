"""
app/api/version.py

Single source of truth for the application version.
Updated automatically by .github/workflows/release.yml.

Exposed at:
  GET /health     → {"status": "ok", "version": "0.1.0"}
  GET /api/v1/    → {"version": "0.1.0", ...}
"""
__version__ = "0.1.0-beta"
__api_version__ = "v1"

VERSION_INFO = {
    "version": __version__,
    "api_version": __api_version__,
    "project": "EduBoost SA",
}
