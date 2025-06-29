# Graph Commits per Project

## Goal

To show on how many different projects I worked this week.

## Process

1. Use `Settings.github_token` (model, effectively singleton) to auth with GitHub
2. For the last 10 weeks, get how many commits I did per project (including only projects where commits happened in this time frame)
3. Visualize this as a *Stacked Area Chart* [Example](https://python-graph-gallery.com/stacked-area-plot/), [Chart JS example](https://www.chartjs.org/docs/latest/samples/area/line-stacked.html) in the template.

## Notes

- Add this view to the nav header
- Utilize the `get_nr_of_commits_per_week_and_project` util