from django.test import TestCase
from django.test.utils import override_settings
from django.core import management, mail

from ..compat import get_user_model
from ..models import create_notice_type, NoticeType, queue


class TestManagementCmd(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test_user", "test@user.com", "123456")
        self.user2 = get_user_model().objects.create_user("test_user2", "test2@user.com", "123456")
        create_notice_type("label", "display", "description")
        self.notice_type = NoticeType.objects.get(label="label")

    @override_settings(SITE_ID=1)
    def test_emit_notices(self):
        users = [self.user, self.user2]
        queue(users, "label")
        management.call_command("emit_notices")
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(self.user.email, mail.outbox[0].to)
        self.assertIn(self.user2.email, mail.outbox[1].to)
