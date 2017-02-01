from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard


class CustomDashboard(Dashboard):
    columns = 3


    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.add_export_dashboard()

    def add_export_dashboard(self):
        self.children.append(modules.LinkList(
            _('其它匯出'),
            children=[
                {
                    'title': _('總廠商列表'),
                    'url': '/admin/company/company/export/',
                    'external': False,
                },
            ],
            column=2,
            order=0
        ))
        self.children.append(modules.LinkList(
            _('校徵匯出'),
            children=[
                {
                    'title': _('匯出全部資料'),
                    'url': '/admin/recruit/export_all/',
                    'external': False,
                },
                {
                    'title':_('匯出說明會資訊'),
                    'url': '/admin/recruit/export_seminar_info/',
                    'external': False,
                },
                
                }
                {
                    'title': _('廠商Logo和簡介(廣告用)'),
                    'url': '/admin/recruit/export_ad/',
                    'external': False,
                },
                {
                    'title': _('廠商滿意度問卷'),
                    'url': '/admin/recruit/companysurvey/export/',
                    'external': False,
                },
            ],
            column=2,
            order=1
        ))

        self.children.append(modules.LinkList(
            _('研替匯出'),
            children=[
                {
                    'title': _('匯出全部資料'),
                    'url': '/admin/rdss/export_all/',
                    'external': False,
                },
                {
                    'title': _('廠商Logo和簡介(廣告用)'),
                    'url': '/admin/rdss/export_ad/',
                    'external': False,
                },
                {
                    'title': _('廠商滿意度問卷'),
                    'url': '/admin/rdss/companysurvey/export/',
                    'external': False,
                },
            ],
            column=2,
            order=1
        ))

        self.children.append(modules.LinkList(
            _('研替集點'),
            children=[
                {
                    'title': _('研替說明會集點'),
                    'url': '/admin/rdss/collect_points/',
                    'external': False,
                },
                {
                    'title': _('學生證註冊'),
                    'url': '/admin/rdss/reg_card/',
                    'external': False,
                },
                {
                    'title': _('兌獎'),
                    'url': '/admin/rdss/redeem/',
                    'external': False,
                },
                {
                    'title': _('讀卡程式及驅動'),
                    'url': '/static/data/apps/card_reader.zip',
                    'external': False,
                },
            ],
            column=2,
            order=1
        ))
