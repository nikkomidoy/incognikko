from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import Education, Experience, HomePage, SkillGroup
from core.resume_content import EDUCATION, PROFILE, SKILL_GROUPS, experience_rows


class Command(BaseCommand):
    help = (
        "Replace the home page's resume with core/resume_content.py and publish it as a new "
        "revision (the previous version stays in the page history)."
    )

    def handle(self, *args, **options):
        page = HomePage.objects.first()
        if page is None:
            raise CommandError("No home page exists yet; run `migrate` first.")
        # Start from the latest revision so an unpublished draft isn't silently lost.
        page = page.get_latest_revision_as_object()

        for field, value in PROFILE.items():
            setattr(page, field, value)
        page.seo_title = PROFILE["headline"]
        # The resume publishes the phone number; the site keeps it hidden until you
        # tick "Show phone" in the admin (public numbers attract spam).

        # Child rows are replaced as a whole: assigning a list to a ParentalKey relation
        # stages them in the revision, and publish writes them to the database.
        page.experiences = [
            Experience(sort_order=i, **row) for i, row in enumerate(experience_rows())
        ]
        page.skill_groups = [
            SkillGroup(sort_order=i, name=name, skills=skills)
            for i, (name, skills) in enumerate(SKILL_GROUPS)
        ]
        page.education = [Education(sort_order=i, **row) for i, row in enumerate(EDUCATION)]
        page.certifications = []  # the current resume lists no certification

        with transaction.atomic():
            revision = page.save_revision(log_action=True)
            revision.publish()

        self.stdout.write(
            self.style.SUCCESS(
                f"Published resume revision {revision.pk}: {len(experience_rows())} roles, "
                f"{len(SKILL_GROUPS)} skill groups, {len(EDUCATION)} education entry."
            )
        )
