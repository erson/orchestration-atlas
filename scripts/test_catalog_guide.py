"""Offline regression checks for the README guide and the weekly link summary."""

import unittest

from scripts import update


class CatalogGuideTests(unittest.TestCase):
    def test_weekly_counts_use_only_indexed_repositories(self):
        projects = [{"repo": f"Org/{name}"} for name in ("Moved", "Gone", "Retry", "Pending")]
        cache = {
            "org/moved": {"full_name": "New/Name", "archived": True},
            "org/gone": {"error": 404},
            "org/retry": {"full_name": "org/retry", "last_error": 502},
            "org/removed": {"archived": True},
        }
        summary = update.weekly_link_summary(projects, cache)
        for label in ("Moved", "Unavailable", "Archived", "Fetch failed with a previous snapshot",
                      "Awaiting a first fetch"):
            self.assertIn(f"{label}: 1", summary)

    def test_guide_uses_the_current_url_and_omits_unavailable_tools(self):
        projects = [{"repo": f"org/{name}", "name": name, "origin": "discovered", "category": "desktop",
                     "guide_task": f"Example for {name}."} for name in ("Live", "Archived", "Gone")]
        doc = {"projects": projects, "categories": [{"id": "desktop", "title": "Desktop"}]}
        rows = update.build_rows(projects, {"org/live": {"url": "https://github.com/new/live"},
                                             "org/archived": {"archived": True}, "org/gone": {"error": 404}})
        readme = update.render_readme(doc, rows, {})
        guide = readme.split("## Choose a task\n", 1)[1].split("| I want to", 1)[0]
        self.assertIn("[Live](https://github.com/new/live)", guide)
        self.assertIn("Example for Live.", guide)
        self.assertNotIn("Example for Archived.", guide)
        self.assertNotIn("Example for Gone.", guide)
