#!/usr/bin/env python3

"""
Caches the results of certain pico API calls in Redis every ~60sec.

Functions as an alternative entrypoint for the API container.

Must be running in order to provide accurate stats, as some memoized API
functions otherwise have no TTL.

The cache-daemon container should not be scaled beyond a single replica.
"""

from time import sleep

import api
from api.stats import (get_all_team_scores, get_group_scores,
                       get_problem_solves, get_registration_count,
                       get_top_teams_score_progressions)


def run():
    """Run the stat caching daemon."""
    with api.create_app().app_context():
        def cache(f, *args, **kwargs):
            result = f(reset_cache=True, *args, **kwargs)
            return result

        while(True):
            print("Caching registration stats...")
            cache(get_registration_count)

            print("Caching the scoreboards...")
            for scoreboard in api.scoreboards.get_all_scoreboards():
                get_all_team_scores(scoreboard_id=scoreboard['sid'])

            print("Caching the score progressions for each scoreboard...")
            for scoreboard in api.scoreboards.get_all_scoreboards():
                cache(get_top_teams_score_progressions,
                      limit=5,
                      scoreboard_id=scoreboard['sid'])

            print(
                  "Caching the scores / score progressions for each group...")
            for group in api.group.get_all_groups():
                get_group_scores(gid=group['gid'])
                cache(get_top_teams_score_progressions,
                      limit=5,
                      group_id=group['gid'])

            print("Caching number of solves for each problem...")
            for problem in api.problem.get_all_problems():
                print(problem["name"],
                      cache(get_problem_solves, problem["pid"]))

            sleep(60)


if __name__ == '__main__':
    run()
