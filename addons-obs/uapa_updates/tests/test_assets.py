#-*- coding: utf-8 -*-
from openerp.tests import common
from datetime import date


class TestAssets(common.TransactionCase):

    def create_assets(self, cr, uid, model_obj, amount):
        """Helper method for creating demo data.

        Args:
            model_obj; openerp object to access orm.
            amount; integer; number of objects to create.

        Return:
            created_ids; list of ids created"""
        res = []
        category_obj = self.registry('account.asset.category')
        company_obj = self.registry('res.company')
        company_id = company_obj.search(cr, uid, [], limit=1)[0]
        category_id = category_obj.search(cr, uid, [], limit=1)[0]
        for asset in range(amount):
            values = {
                'name': 'Test Asset {0}'.format(asset),
                'category_id': category_id,
                'company_id': company_id,
                'purchase_date': date.today().isoformat(),
                'code': 'ASS-0{0}'.format(asset),
                'purchase_value': 3000 * asset,
                'method': 'linear',
                'method_time': 'number',
                'method_number': 48,
                'method_period': 12,
                'state': 'open',
            }
            res.append(model_obj.create(cr, uid, values))
        return res


    def setUp(self):
        super(TestAssets, self).setUp()

        cr, uid = self.cr, self.uid
        self.asset_obj = self.registry('account.asset.asset')
        self.depreciation_obj = self.registry('account.asset.depreciation.line')
        self.move_obj = self.registry('account.move')
        self.move_line_obj = self.registry('account.move.line')

        #Creating demo data.
        self.assets = self.create_assets(cr, uid, self.asset_obj, 5)
        #Calculating all the depreciation tables
        self.asset_obj.compute_depreciation_board(cr, uid, self.assets)

    def testCheckValidPeriod(self):
        """Check that a valid period for the asset can be found."""
        cr, uid = self.cr, self.uid
        asset = self.asset_obj.read(cr, uid, self.assets[1])
        period_obj = self.registry('account.period')
        line = asset.get('depreciation_line_ids')[0]
        period_found = self.asset_obj.get_period(cr, uid, line)
        self.assertTrue(period_obj.read(cr, uid, period_found))

    def testMovesCreated(self):
        """Check that an valid account.move is created from an asset."""
        cr, uid = self.cr, self.uid
        move_obj = self.registry('account.move')
        asset = self.asset_obj.read(cr, uid, self.assets[1])
        self.asset_obj.run_asset_entry(cr, uid)
        result = move_obj.search(cr, uid, [('name', '=', asset.get('name'))])
        self.assertTrue(result)

    def testAccountMoveValues(self):
        """Check that we are using the correct parameters to create an account
        movement."""
        cr, uid = self.cr, self.uid
        asset = self.assets[1]
        asset_values = self.asset_obj.read(cr, uid, asset)
        journal_id = self.asset_obj.browse(cr, uid, asset).category_id.journal_id.id
        for line in asset_values.get('depreciation_line_ids'):
            period_id = self.asset_obj.get_period(cr, uid, line)
            expected_values = {
                'name': asset_values.get('name').encode('utf-8'),
                'period_id': period_id,
                'date': date.today().isoformat(),
                'state': 'draft',
                'ref': asset_values.get('name').encode('utf-8'),
                'journal_id': journal_id,
                'company_id': asset_values.get('company_id')[0]
            }
            if period_id:
                values = self.asset_obj.prepare_account_move(cr, uid, line, period_id)
                self.assertDictEqual(values, expected_values)
            else:
                continue

    def testAccountMoveDebit(self):
        """Check that the correct values are being used for creating the account
        movemente debit."""
        cr, uid = self.cr, self.uid
        currency_obj = self.registry('res.currency')
        asset = self.assets[1]
        asset_values = self.asset_obj.read(cr, uid, asset)
        asset_browse = self.asset_obj.browse(cr, uid, asset)
        account = asset_browse.category_id.account_depreciation_id
        journal = asset_browse.category_id.journal_id
        company_currency = asset_browse.company_id.currency_id.id
        asset_currency = asset_browse.currency_id.id
        sign = (asset_browse.category_id.journal_id.type == 'purchase' and 1) or -1
        amount_currency = (company_currency != asset_currency and - sign *
                           line.amount or 0.0)
        for line in asset_values.get('depreciation_line_ids'):
            period_id = self.asset_obj.get_period(cr, uid, line)
            if not period_id:
                break
            move_values = self.asset_obj.prepare_account_move(cr, uid, line, period_id)
            move_id = self.move_obj.create(cr, uid, move_values)
            line_values = self.depreciation_obj.read(cr, uid, line)
            amount = currency_obj.compute(cr, uid, asset_currency,
                                          company_currency, line_values.get('amount'))
            expected_values = {
                'name': asset_values.get('name').encode('utf-8'),
                'partner_id': asset_values.get('partner_id') ,
                'debit': amount,
                'credit': 0.0,
                'ref': line_values.get('name').encode('utf-8'),
                'move_id': move_id,
                'account_id': account.id,
                'journal_id': journal.id,
                'currency_id': company_currency != asset_currency and asset_currency or False,
                'date': date.today().isoformat(),
                'amount_currency': amount_currency,
                'period_id': period_id,
                'company_id': asset_values.get('company_id')[0]
            }
            values = self.asset_obj.prepare_move_line(cr, uid, line, move_id,
                                                      period_id, move_type='debit')
            self.assertDictEqual(values, expected_values)

    def testAccountMoveCredit(self):
        """Check that the correct values are being used for creating the account
        movemente credit."""
        cr, uid = self.cr, self.uid
        currency_obj = self.registry('res.currency')
        asset = self.assets[1]
        asset_values = self.asset_obj.read(cr, uid, asset)
        asset_browse = self.asset_obj.browse(cr, uid, asset)
        account = asset_browse.category_id.account_expense_depreciation_id
        journal = asset_browse.category_id.journal_id
        company_currency = asset_browse.company_id.currency_id.id
        asset_currency = asset_browse.currency_id.id
        sign = (asset_browse.category_id.journal_id.type == 'purchase' and 1) or -1
        amount_currency = (company_currency != asset_currency and - sign *
                           line.amount or 0.0)
        for line in asset_values.get('depreciation_line_ids'):
            period_id = self.asset_obj.get_period(cr, uid, line)
            if not period_id:
                break
            move_values = self.asset_obj.prepare_account_move(cr, uid, line, period_id)
            move_id = self.move_obj.create(cr, uid, move_values)
            line_values = self.depreciation_obj.read(cr, uid, line)
            amount = currency_obj.compute(cr, uid, asset_currency,
                                          company_currency, line_values.get('amount'))
            expected_values = {
                'name': asset_values.get('name'),
                'partner_id': asset_values.get('partner_id') ,
                'debit': 0.0,
                'credit': amount,
                'ref': line_values.get('name'),
                'move_id': move_id,
                'account_id': account.id,
                'journal_id': journal.id,
                'currency_id': company_currency != asset_currency and asset_currency or False,
                'date': date.today().isoformat(),
                'amount_currency': amount_currency,
                'period_id': period_id,
                'company_id': asset_values.get('company_id')[0]
            }
            values = self.asset_obj.prepare_move_line(cr, uid, line, move_id,
                                                      period_id, move_type='credit')
            self.assertDictEqual(values, expected_values)

    def testJournalCompanyPositive(self):
        """Check for True when the journal has the same company as the
        asset."""
        cr, uid = self.cr, self.uid
        asset_category = self.registry('account.asset.category')
        asset_values = self.asset_obj.read(cr, uid, self.assets[1])
        journal_company = asset_category.browse(cr, uid, asset_values.get('category_id')[0]).journal_id.company_id
        self.assertEqual(asset_values.get('company_id')[0], journal_company.id)

    def test_asset_ids(self):
        """Check that ids returned by the query are the same as the ones
        returned by the orm method."""
        cr, uid = self.cr, self.uid
        expected_ids = self.asset_obj.search(cr, uid, [('active','=',True),
                                             ('state','=','open')])
        result = self.asset_obj.get_asset_ids(cr)
        self.assertEqual(expected_ids, result)
