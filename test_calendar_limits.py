import unittest
from app import run

class CalendarLimitsTest(unittest.TestCase):
    def data(self, count=1, start='9999-12-31', weeks=1, blocked=None):
        return {'inicio':start, 'intervalo_semanas':weeks, 'bloqueios':blocked or [],
                'mensagens':[{'titulo':'Mensagem', 'referencia':'João 15'} for _ in range(count)]}

    def test_last_valid_date_does_not_require_next_date(self):
        self.assertEqual(run(self.data())['ultima_data'], '9999-12-31')

    def test_overflow_for_second_message_is_validation_error(self):
        with self.assertRaises(ValueError):
            run(self.data(count=2))

    def test_blocked_max_date_is_validation_error(self):
        with self.assertRaises(ValueError):
            run(self.data(blocked=['9999-12-31']))

    def test_unrepresentable_interval_is_validation_error(self):
        with self.assertRaises(ValueError):
            run(self.data(weeks=10**20))

    def test_consecutive_blocked_dates_are_skipped(self):
        value=run(self.data(count=2,start='2026-12-06',blocked=['2026-12-06','2026-12-13']))
        self.assertEqual([x['data'] for x in value['agenda']], ['2026-12-20','2026-12-27'])
