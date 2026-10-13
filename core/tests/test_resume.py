import html as html_lib

import pytest
from django.core.management import call_command

from core.models import Certification, Experience, HomePage
from core.resume_content import EDUCATION, EXPERIENCES, PROFILE, SKILL_GROUPS


def page_text(client) -> str:
    return html_lib.unescape(client.get("/").text)


@pytest.mark.django_db
def test_home_shows_resume_word_for_word(client):
    text = page_text(client)
    for heading in ("Professional Summary", "Core Skills", "Work Experience", "Education"):
        assert heading in text
    assert PROFILE["headline"] in text and PROFILE["summary"] in text
    for exp in EXPERIENCES:
        assert exp["role"] in text and exp["company"] in text
        assert all(bullet in text for bullet in exp["highlights"])
    for name, skills in SKILL_GROUPS:
        assert name in text
        assert all(skill.strip() in text for skill in skills.split(","))
    assert "Feb 2023 to Sep 2026" in text
    assert "Deel Inc. (Client: Prezzee)" in text
    assert f"{EDUCATION[0]['school']}, Davao | 2010 to 2014" in text
    assert PROFILE["phone"] not in text  # stored, but hidden until "Show phone" is ticked


@pytest.mark.django_db
def test_load_resume_publishes_a_new_revision(client):
    page = HomePage.objects.get()
    page.headline = "Old headline"
    page.save_revision().publish()
    Certification.objects.create(page=page, name="Old certificate")
    revisions_before = page.revisions.count()

    call_command("load_resume")

    page = HomePage.objects.get()
    assert page.headline == PROFILE["headline"]
    assert page.revisions.count() == revisions_before + 1
    # The admin editor opens the latest revision; it must hold the new content too,
    # or the next Publish in the admin would bring the old resume back.
    latest = page.get_latest_revision_as_object()
    assert latest.headline == PROFILE["headline"]
    assert [e.company for e in latest.experiences.all()] == [e["company"] for e in EXPERIENCES]
    assert Experience.objects.filter(page=page).count() == len(EXPERIENCES)
    assert not Certification.objects.exists()
    assert "Old certificate" not in page_text(client)

    call_command("load_resume")  # idempotent: same content, one more revision
    assert Experience.objects.filter(page=page).count() == len(EXPERIENCES)
