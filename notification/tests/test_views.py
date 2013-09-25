from django.test import TestCase
from django.core.urlresolvers import reverse

from ..compat import get_user_model
from ..models import create_notice_type, NoticeSetting, NoticeType, NOTICE_MEDIA


class TestViews(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test_user", "test@user.com", "123456")

    def test_notice_settings_login_required(self):
        url = reverse("notification_notice_settings")
        response = self.client.get(url)
        self.assertRedirects(response, "/accounts/login/?next={}".format(url),
                             target_status_code=404)

    def test_notice_settings(self):
        create_notice_type("label_1", "display", "description")
        notice_type_1 = NoticeType.objects.get(label="label_1")
        create_notice_type("label_2", "display", "description")
        notice_type_2 = NoticeType.objects.get(label="label_2")
        setting = NoticeSetting.for_user(self.user, notice_type_2, NOTICE_MEDIA[0][0])
        setting.send = False
        setting.save()
        self.client.login(username="test_user", password="123456")
        response = self.client.get(reverse("notification_notice_settings"))
        self.assertEqual(response.status_code, 200)

        post_data = {
            "label_2_{}".format(NOTICE_MEDIA[0][0]): "on",
        }
        response = self.client.post(reverse("notification_notice_settings"), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(NoticeSetting.for_user(self.user, notice_type_1, NOTICE_MEDIA[0][0]).send)
        self.assertTrue(NoticeSetting.for_user(self.user, notice_type_2, NOTICE_MEDIA[0][0]).send)
