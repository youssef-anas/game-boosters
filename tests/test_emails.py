import re
from django.test import TestCase, override_settings
from django.core import mail

from accounts.models import BaseUser, BaseOrder, Transaction
from games.models import Game


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class EmailSignalTests(TestCase):
    def setUp(self):
        self.client_user = BaseUser.objects.create_user(username='client', email='client@example.com', password='x', is_customer=True)
        self.booster_user = BaseUser.objects.create_user(username='booster', email='booster@example.com', password='x', is_booster=True)
        self.manager_user = BaseUser.objects.create_user(username='manager', email='manager@example.com', password='x', is_staff=True)
        self.game = Game.objects.create(name='League of Legends', link='/lol', price=10)
        self.order = BaseOrder.objects.create(
            name='ORD-1',
            details='Details',
            game=self.game,
            game_type='D',
            price=100,
            actual_price=80,
            real_order_price=100,
            invoice='INV-1',
            customer=self.client_user,
            booster=self.booster_user,
        )

    def assert_email(self, subject_contains: str, to_contains: str, body_contains: str):
        self.assertTrue(mail.outbox, 'No emails sent')
        found = False
        for m in mail.outbox:
            if subject_contains in m.subject and to_contains in ','.join(m.to) and re.search(body_contains, ''.join([m.body] + [a[1].decode() if hasattr(a[1], 'decode') else a[1] for a in m.alternatives]) if m.alternatives else m.body, re.I):
                found = True
                break
        self.assertTrue(found, f"Expected email not found: subject~{subject_contains}, to~{to_contains}, body~{body_contains}")

    def test_client_payment_confirmation_on_withdrawal_done(self):
        Transaction.objects.create(user=self.client_user, amount=100, order=self.order, status='Done', type='WITHDRAWAL', notice='pay')
        self.assert_email('Payment Confirmation', 'client@example.com', r'Payment Received')

    def test_booster_payout_confirmation_on_deposit_done(self):
        Transaction.objects.create(user=self.booster_user, amount=80, order=self.order, status='Done', type='DEPOSIT', notice='payout')
        self.assert_email('Payout Confirmation', 'booster@example.com', r'Payout Confirmation')

    def test_admin_alert_on_payment_drop(self):
        Transaction.objects.create(user=self.client_user, amount=100, order=self.order, status='Drop', type='WITHDRAWAL', notice='drop')
        # Default from email receives admin alerts
        self.assertTrue(any('Admin Alert' in m.subject for m in mail.outbox))

    def test_manager_alert_on_escalation_status(self):
        mail.outbox.clear()
        self.order.status = 'Escalated'
        self.order.save()
        # Manager/staff should receive an alert
        self.assertTrue(any('Manager Alert' in m.subject for m in mail.outbox))

    def test_manager_alert_when_booster_missing(self):
        mail.outbox.clear()
        self.order.booster = None
        self.order.status = 'New'
        self.order.save()
        self.assertTrue(any('Booster Requested' in m.subject for m in mail.outbox))


