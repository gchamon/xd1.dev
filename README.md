# xd1.dev

This is the repository that is the source of truth for my blog hosted at <https://xd1.dev>.

The automation is based on the upstream repo, but is heavily modified to make it easy for me to upload images to github and have them reflected in the blog, as well as
fixing some quirks in the way that weblog handles markdown, so that it plays well with prism.js for displaying code with syntax highlight.

## mkweblog.sh

This script makes it easier to create weblog posts. It expects three arguments,
the filename (without .md), the title and optionally some tags. Example:

```bash
./mkweblog.sh not-buying-american "Not buying american anymore" "rant, opinion"
```

## Hacker News discussions

Hacker News has a public read API but no documented API for creating stories
([official API documentation](https://github.com/HackerNews/API)). Submission
must be done manually from the HN account.

To link a post's discussion:

1. Add `HN: submit` to the post's front matter and push the post so it is
   published.
2. Submit its canonical URL, `https://xd1.dev/YYYY/MM/<title-slug>`, through
   Hacker News using the account configured in the repository Actions variable
   `HN_USERNAME`.
3. Copy the numeric item ID from the resulting HN URL and run the **HN
   discussion** workflow with the repository-relative post path (for example,
   `weblog/my-post.md`) and item ID.

The workflow verifies that the item is a story by the configured account and
links to the exact post URL, then commits the discussion link and publishes the
updated post. The workflow cannot create the HN story.

## Force a full weblog resync

The deploy workflow normally syncs only files changed in the latest commit. If the
remote weblog state gets out of sync or a bad template/config needs to be replaced
everywhere, commit a change to [`configuration/reset`](/home/gchamon/Projects/xd1.dev/configuration/reset).
When [`weblog-import.php`](/home/gchamon/Projects/xd1.dev/weblog-import.php) sees that file in the pushed diff,
it calls the omg.lol reset endpoint and re-uploads every tracked file in the repo.

Update the reset marker with a fresh timestamp, then commit and push:

```bash
printf 'reset %s\n' "$(date +%Y-%m-%dT%H-%M)" > configuration/reset
```

Rerunning an old GitHub Actions job is not enough by itself; the reset file must be
part of a new commit so the importer enters its full rebuild path.
