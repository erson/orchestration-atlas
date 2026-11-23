"""Regression tests for late release observations."""

import unittest

from scripts import history


class ReleaseHistoryTests(unittest.TestCase):
    def setUp(self):
        self.data = {"projects": {}, "weeks": []}
        self.row = {"repo": "Org/Project", "status": "Active"}
        self.start = "2026-11-16T12:00:00Z"
        self.end = "2026-11-23T12:00:00Z"
        self.next_end = "2026-11-30T12:00:00Z"
        history.observe(self.data, [self.row], self.start)
        history.observe(self.data, [self.row], self.end)

    def test_release_found_after_snapshot_is_kept_in_its_original_period(self):
        release = {**self.row, "latest_release_at": "2026-11-20T10:00:00Z"}
        self.assertFalse(history.observe(self.data, [release], "2026-11-24T12:00:00Z"))
        self.assertTrue(history.reconcile_releases(self.data, [release]))
        self.assertFalse(history.reconcile_releases(self.data, [{**release, "repo": "org/project"}]))

        next_release = {**self.row, "latest_release_at": "2026-11-26T10:00:00Z"}
        history.observe(self.data, [next_release], self.next_end)
        self.assertTrue(history.reconcile_releases(self.data, [next_release]))
        self.assertEqual([[], ["Org/Project"], ["Org/Project"]],
                         [week["released"] for week in self.data["weeks"]])

    def test_release_at_snapshot_boundary_is_counted_only_in_ending_period(self):
        history.observe(self.data, [self.row], self.next_end)
        release = {**self.row, "latest_release_at": self.end}
        self.assertTrue(history.reconcile_releases(self.data, [release]))
        self.assertEqual([[], ["Org/Project"], []], [week["released"] for week in self.data["weeks"]])

    def test_new_projects_do_not_fill_periods_before_they_were_indexed(self):
        new = {"repo": "Org/New", "status": "Active", "latest_release_at": self.end}
        self.assertFalse(history.reconcile_releases(self.data, [self.row, new]))
        history.observe(self.data, [self.row, new], self.next_end)
        self.assertFalse(history.reconcile_releases(self.data, [self.row, new]))
