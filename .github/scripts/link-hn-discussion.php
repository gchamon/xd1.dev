<?php

declare(strict_types=1);

function fail(string $message): never
{
    fwrite(STDERR, $message . PHP_EOL);
    exit(1);
}

$postPath = getenv('POST_PATH');
$itemId = getenv('HN_ITEM_ID');
$username = getenv('HN_USERNAME');

if ($postPath === false || !preg_match('#^weblog/[A-Za-z0-9][A-Za-z0-9._/-]*\.md$#', $postPath) || str_contains($postPath, '..')) {
    fail('POST_PATH must name a Markdown post within weblog/.');
}
if ($itemId === false || !preg_match('/^[0-9]+$/', $itemId)) {
    fail('HN_ITEM_ID must be a numeric Hacker News item ID.');
}
if ($username === false || trim($username) === '') {
    fail('Set the repository Actions variable HN_USERNAME to the HN account used to submit stories.');
}
if (!is_file($postPath)) {
    fail("Post does not exist: $postPath");
}

$content = file_get_contents($postPath);
if ($content === false) {
    fail("Could not read post: $postPath");
}
if (!preg_match('/\A---\R(.*?)\R---\R/s', $content, $frontMatter, PREG_OFFSET_CAPTURE)) {
    fail('Post must contain exactly one YAML-style front matter block at the start.');
}
$header = $frontMatter[1][0];
if (preg_match_all('/^HN:\s*(.*?)\s*$/m', $header, $hnMatches, PREG_OFFSET_CAPTURE) !== 1 || $hnMatches[1][0][0] !== 'submit') {
    fail('Post front matter must contain exactly one `HN: submit` field.');
}
if (preg_match_all('/^Date:\s*(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})\s*$/m', $header, $dateMatches) !== 1) {
    fail('Post front matter must contain exactly one Date in YYYY-MM-DD HH:MM format.');
}
$year = $dateMatches[1][0];
$month = $dateMatches[2][0];
$day = $dateMatches[3][0];
$hour = $dateMatches[4][0];
$minute = $dateMatches[5][0];
if (!checkdate((int)$month, (int)$day, (int)$year) || (int)$hour > 23 || (int)$minute > 59) {
    fail('Post Date is not a valid calendar date and time.');
}
if (!preg_match('/^#\s+(.+?)\s*$/m', substr($content, $frontMatter[0][1] + strlen($frontMatter[0][0])), $titleMatch)) {
    fail('Post must contain an H1 title after its front matter.');
}
$title = trim($titleMatch[1]);
$slug = strtolower($title);
$slug = preg_replace('/[^a-z0-9]+/', '-', $slug);
$slug = trim((string)$slug, '-');
if ($slug === '') {
    fail('Post H1 does not produce a usable ASCII URL slug.');
}
$postUrl = sprintf('https://xd1.dev/%04d/%02d/%s', (int)$year, (int)$month, $slug);

$itemUrl = 'https://hacker-news.firebaseio.com/v0/item/' . $itemId . '.json';
$context = stream_context_create(['http' => ['timeout' => 15, 'ignore_errors' => true, 'header' => "User-Agent: xd1.dev HN discussion linker\r\n"]]);
$response = @file_get_contents($itemUrl, false, $context);
if ($response === false) {
    fail('Could not retrieve the HN item; no post changes were made.');
}
$item = json_decode($response, true);
if (!is_array($item) || json_last_error() !== JSON_ERROR_NONE || !isset($item['type'], $item['by'], $item['url'])) {
    fail('HN returned an invalid item record; no post changes were made.');
}
if ($item['type'] !== 'story' || $item['by'] !== $username || $item['url'] !== $postUrl) {
    fail('HN item must be a story submitted by HN_USERNAME with the exact post URL; no post changes were made.');
}
if (str_contains($content, 'news.ycombinator.com/item?id=')) {
    fail('Post already contains an HN item link; refusing to duplicate or overwrite it.');
}
$hnValueOffset = $frontMatter[0][1] + 4 + $hnMatches[1][0][1];
$hnValueLength = strlen($hnMatches[1][0][0]);
$discussionUrl = 'https://news.ycombinator.com/item?id=' . $itemId;
$content = substr_replace($content, $discussionUrl, $hnValueOffset, $hnValueLength);

$invitation = "Join the discussion on [Hacker News]($discussionUrl).";
if (preg_match('/^## Comments\s*$/m', $content, $commentsMatch, PREG_OFFSET_CAPTURE)) {
    $insertAt = $commentsMatch[0][1] + strlen($commentsMatch[0][0]);
    $content = substr_replace($content, "\n\n$invitation", $insertAt, 0);
} else {
    $content = rtrim($content) . "\n\n## Comments\n\n$invitation\n";
}
if (file_put_contents($postPath, $content, LOCK_EX) === false) {
    fail("Could not write post: $postPath");
}
echo "Linked $postPath to $discussionUrl" . PHP_EOL;
