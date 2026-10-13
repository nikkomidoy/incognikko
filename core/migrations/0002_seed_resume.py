"""Seed the Wagtail page tree with the resume and the privacy page.

Resume text comes from core/resume_content.py (shared with `manage.py load_resume`).

Replaces Wagtail's default "Welcome" page with a HomePage at the site root. Runs once;
skipped if a HomePage already exists. Everything is editable afterwards in /admin/.
"""

import json
import uuid
from datetime import date

from django.db import migrations
from django.utils import timezone

from core.resume_content import EDUCATION, PROFILE, SKILL_GROUPS, experience_rows

PRIVACY_POLICY = """_Last updated: October 2026_

This site is a personal portfolio and blog. It is built to collect as little personal data as possible.

## What is collected

- **Analytics (no cookies).** Page views are counted with [GoatCounter](https://www.goatcounter.com/), which sets no cookies and does not track you across sites. It records the page, referrer, browser/OS family, screen size and country derived from your IP address; the IP itself is not stored.
- **Server logs.** Requests are logged for security and debugging **without your IP address**. Logs are rotated and kept for a short period.
- **Error reports.** If a page crashes, a technical error report is sent to Sentry with cookies and authorization headers stripped and no personal data attached.
- **Accounts (optional).** If you create an account, your username, email address and a hashed password are stored. Failed login attempts (username, IP address, time) are recorded to block brute-force attacks and are **deleted automatically after 30 days**.

## Cookies

The site sets no tracking or advertising cookies. Strictly necessary cookies are only set when you submit a form or sign in (`csrftoken`, `sessionid`). No consent banner is needed for these.

## Facebook

New blog posts are shared to a Facebook Page. This site does not embed Facebook scripts, pixels or "like" buttons, so Facebook receives nothing from your visit here. If you follow a link to Facebook, Facebook's own privacy policy applies there.

## Where data is stored

The site is hosted on Amazon Web Services. Uploaded images and database backups are stored in private Amazon S3 buckets.

## Your rights (GDPR / PIPEDA)

You can ask for a copy of your data, its correction, or its deletion at any time by emailing the address below. Account data is exported or erased within 30 days of a verified request.

## Contact

nikkomidoy@gmail.com
"""



def markdown_stream(text: str) -> str:
    return json.dumps([{"type": "markdown", "value": text, "id": str(uuid.uuid4())}])


def page_fields(apps, model: str, *, title: str, slug: str, path: str, url_path: str, **extra):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Locale = apps.get_model("wagtailcore", "Locale")
    app_label, model_name = model.split(".")
    now = timezone.now()
    return {
        "title": title,
        "draft_title": title,
        "slug": slug,
        "content_type": ContentType.objects.get_or_create(app_label=app_label, model=model_name)[0],
        "path": path,
        "depth": len(path) // 4,
        "url_path": url_path,
        "locale": Locale.objects.order_by("pk").first(),
        "translation_key": uuid.uuid4(),
        "live": True,
        "has_unpublished_changes": False,
        "first_published_at": now,
        "last_published_at": now,
        **extra,
    }


def seed(apps, schema_editor):
    HomePage = apps.get_model("core", "HomePage")
    if HomePage.objects.exists():
        return
    Page = apps.get_model("wagtailcore", "Page")
    Site = apps.get_model("wagtailcore", "Site")

    # Wagtail's stock "Welcome to your new Wagtail site!" page (its Site cascades with it).
    Page.objects.filter(
        depth=2, content_type__app_label="wagtailcore", content_type__model="page"
    ).delete()
    root = Page.objects.get(depth=1)

    home = HomePage.objects.create(
        **page_fields(
            apps,
            "core.homepage",
            title="Nikko Comidoy",
            slug="home",
            path=root.path + "0001",
            url_path="/home/",
            seo_title=PROFILE["headline"],
            numchild=1,
        ),
        **PROFILE,
        show_email=True,
        show_phone=False,
    )
    Page.objects.filter(pk=root.pk).update(numchild=Page.objects.filter(depth=2).count())
    Site.objects.create(
        hostname="localhost", port=80, root_page_id=home.pk, is_default_site=True
    )

    Experience = apps.get_model("core", "Experience")
    for i, exp in enumerate(experience_rows()):
        Experience.objects.create(page=home, sort_order=i, **exp)

    SkillGroup = apps.get_model("core", "SkillGroup")
    for i, (name, skills) in enumerate(SKILL_GROUPS):
        SkillGroup.objects.create(page=home, sort_order=i, name=name, skills=skills)

    for i, edu in enumerate(EDUCATION):
        apps.get_model("core", "Education").objects.create(page=home, sort_order=i, **edu)
    apps.get_model("core", "ContentPage").objects.create(
        **page_fields(
            apps,
            "core.contentpage",
            title="Privacy policy",
            slug="privacy",
            path=home.path + "0001",
            url_path="/home/privacy/",
            search_description="How this site handles personal data.",
        ),
        body=markdown_stream(PRIVACY_POLICY),
        show_in_footer=True,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("wagtailcore", "0098_apitoken"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]
