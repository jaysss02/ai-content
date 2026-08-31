"""Canned content used by DEMO_MODE so the pipeline runs with zero setup.

Templates are filled in with the brief's fields. They're deliberately
generic - good enough to see the pipeline work end to end, not meant to
read like real API output.
"""

from __future__ import annotations

from .models import Brief, Newsletter

BLOG_TEMPLATE = """# {topic}

If you're part of {audience}, {topic_lower} probably isn't news to you - but
here's what's worth paying attention to right now.

{key_points_section}

Bottom line: this matters for {audience}, and getting ahead of it is easier
than catching up later.

*[DEMO MODE - set ANTHROPIC_API_KEY to generate real content]*
"""

INSTAGRAM_TEMPLATE = """{hook}

{key_points_bullets}

Tell us in the comments how this shows up for you. #{hashtag}

[DEMO MODE - set ANTHROPIC_API_KEY to generate real content]
"""

NEWSLETTER_SUBJECT_TEMPLATE = "What {audience} should know about {topic}"

NEWSLETTER_BODY_TEMPLATE = """Hi there,

This week we're digging into {topic_lower}.

{key_points_section}

That's it for this week - reply and let us know what you think.

[DEMO MODE - set ANTHROPIC_API_KEY to generate real content]
"""


def _key_points_section(brief: Brief) -> str:
    return "\n".join(f"- {point}" for point in brief.key_points)


def _key_points_bullets(brief: Brief) -> str:
    return "\n".join(f"* {point}" for point in brief.key_points)


def demo_blog(brief: Brief) -> str:
    return BLOG_TEMPLATE.format(
        topic=brief.topic,
        topic_lower=brief.topic[:1].lower() + brief.topic[1:],
        audience=brief.target_audience,
        key_points_section=_key_points_section(brief),
    )


def demo_instagram(brief: Brief) -> str:
    hashtag = "".join(word.capitalize() for word in brief.topic.split())
    return INSTAGRAM_TEMPLATE.format(
        hook=f"{brief.topic}? Here's what {brief.target_audience} need to know.",
        key_points_bullets=_key_points_bullets(brief),
        hashtag=hashtag or "ContentAutomation",
    )


def demo_newsletter(brief: Brief) -> Newsletter:
    return Newsletter(
        subject=NEWSLETTER_SUBJECT_TEMPLATE.format(
            audience=brief.target_audience, topic=brief.topic
        ),
        body=NEWSLETTER_BODY_TEMPLATE.format(
            topic_lower=brief.topic[:1].lower() + brief.topic[1:],
            topic=brief.topic,
            key_points_section=_key_points_section(brief),
        ),
    )
