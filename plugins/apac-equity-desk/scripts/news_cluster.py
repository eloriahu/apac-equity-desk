"""Cluster near-duplicate headlines so repetitions do not masquerade as independent evidence."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from common import load_data, parse_timestamp, parser, records, write_output

STOP = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is", "of", "on", "or", "the", "to", "with"}


def tokens(text: str) -> set[str]:
    return {word for word in re.findall(r"[\w\u3400-\u9fff]+", text.lower()) if len(word) > 1 and word not in STOP}


def similarity(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left or right else 0.0


_UNDATED = datetime.max.replace(tzinfo=timezone.utc)


def _published(row: dict[str, Any]) -> datetime:
    # Compare instants, not strings: "02:00Z" is later than "09:00+08:00".
    return parse_timestamp(row.get("published_at")) or _UNDATED


def cluster_news(articles: list[dict[str, Any]], threshold: float = 0.55) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    for article in sorted(articles, key=_published):
        title_tokens = tokens(str(article.get("title", "")))
        article_tokens = tokens(f"{article.get('title', '')} {article.get('body', '')}")
        match = None
        for cluster in clusters:
            if max(similarity(title_tokens, cluster["_title_tokens"]), similarity(article_tokens, cluster["_tokens"])) >= threshold:
                match = cluster
                break
        if match is None:
            clusters.append({"_title_tokens": title_tokens, "_tokens": article_tokens, "articles": [article]})
        else:
            match["articles"].append(article)
            match["_title_tokens"] |= title_tokens
            match["_tokens"] |= article_tokens
    result: list[dict[str, Any]] = []
    for index, cluster in enumerate(clusters, 1):
        members = cluster["articles"]
        levels = [int(row["evidence_level"]) for row in members if str(row.get("evidence_level", "")).isdigit()]
        result.append({
            "cluster_id": f"n{index}",
            "representative_title": members[0].get("title"),
            "earliest_published_at": members[0].get("published_at"),
            "article_count": len(members),
            # Outlets that carried the story. A cluster is one underlying story, so
            # these are not independent confirmations of each other.
            "independent_sources": sorted({str(row.get("source", "unknown")) for row in members}),
            "undated_article_ids": [row.get("id") for row in members if parse_timestamp(row.get("published_at")) is None],
            "best_evidence_level": min(levels) if levels else None,
            "article_ids": [row.get("id") for row in members],
        })
    return result


if __name__ == "__main__":
    cli = parser(__doc__)
    cli.add_argument("--threshold", type=float, default=0.55)
    args = cli.parse_args()
    write_output(cluster_news(records(load_data(args.input)), args.threshold), args.output)
