# -*- coding: utf-8 -*-
#
from openerp.osv import fields, orm, osv
from datetime import date
import time
import logging
_logger = logging.getLogger(__name__)


class account_invoice_line(osv.osv):

    _inherit = 'account.invoice.line'

    _columns = {
        'asset_category_id': fields.many2one('account.asset.category', 'Asset Category'),
    }

    def asset_create(self, cr, uid, lines, context=None):
        context = context or {}
        asset_obj = self.pool.get('account.asset.asset')
        asset_asset_obj = self.pool.get('asset.asset')
        for line in lines:
            quantity = int(round(line.quantity))
            if line.asset_category_id:
                for i in range(quantity):
                    taxes = line.invoice_line_tax_id
                    tax_line_amount = 0
                    for tax in taxes:
                        if tax.itbis and (not tax.price_include or not tax.exempt):
                            tax_line_amount += (line.price_unit * tax.amount)
                        else:
                            tax_line_amount += 0
                    asset_asset_vals = {
                        'name': line.name,
                        'vendor_id': line.partner_id.id,
                        'purchase_date': line.invoice_id.date_invoice,
                    }
                    vals = {
                        'name': line.name,
                        'code': line.invoice_id.number or False,
                        'asset_id': asset_asset_obj.create(cr, uid, asset_asset_vals, context=context),
                        'category_id': line.asset_category_id.id,
                        'purchase_value': (line.price_subtotal + tax_line_amount),
                        'period_id': line.invoice_id.period_id.id,
                        'partner_id': line.invoice_id.partner_id.id,
                        'company_id': line.invoice_id.company_id.id,
                        'currency_id': line.invoice_id.currency_id.id,
                        'purchase_date' : line.invoice_id.date_invoice,
                    }
                    changed_vals = asset_obj.onchange_category_id(cr, uid, [], vals['category_id'], context=context)
                    vals.update(changed_vals['value'])
                    asset_id = asset_obj.create(cr, uid, vals, context=context)
                    if line.asset_category_id.open_asset:
                        asset_obj.validate(cr, uid, [asset_id], context=context)
        return True


class UpdateAssetName(osv.osv):
    #_name = 'update.event.registration.fields'
    _inherit = 'account.asset.asset'

    def update_asset_name(self, cr, uid, ids, context=None):
        account_assent_asset_obj = self.pool.get('account.asset.asset')
        assent_asset_obj = self.pool.get('asset.asset')

        asset_no_name = account_assent_asset_obj.search(cr, uid, [('name', '=', False)])

        asset_no_names = account_assent_asset_obj.browse(cr, uid, asset_no_name)

        contador = 0
        for item in asset_no_names:

            asset_asset = assent_asset_obj.search(cr, uid, [('id', '=', item.asset_id.id)])
            assets_assets = assent_asset_obj.browse(cr, uid, asset_asset)
            account_assent_asset_obj.write(cr, uid, item.id,
                                         {'name': assets_assets.name}, context=context)
            contador += 1
            print contador

class AccountAssets(orm.Model):

    _inherit = 'account.asset.asset'

    def get_depreciation_number(self, cr, uid, ids, purchase_value,
        life_expectancy, method_period, context=None):
        """Calculates the number of depreciations based on the formula.
        (purchase_value / ((purchase_value / life_expectancy) / 12 )) / method_period

        Args:
            purchase_value; float, the value of the asset.
            life_expectancy; float, the expected life of the asset.
            method_period; integer, the number of months in a period of
            depreciation

        Returns:
            result; dict, {asset_id: depreciation_number}
            depreciation_number; integer, the number of times the asset is
            going to be deprecated in the period.
        """
        result = {}
        if not purchase_value and not life_expectancy:
            #This occurs when we create the asset, so we return value 0.
            #For avoiding a nasty Erro Message.
            result['value'] = {'method_number': 5}
            return result
        try:
            depreciation_number = (purchase_value / ((purchase_value / life_expectancy) / 12)) / method_period
            result['value'] = {
            'method_number': depreciation_number
            }
        except ZeroDivisionError, error:
            raise orm.except_orm('Error', "{0}".format(error))
        return result

    def get_asset_code(self, cr, uid, ids, field_name, args, context=None):
        """Get the codes for the asset category and res_company and append it
        to the sequence code of the company assets. It writes this values
        to the field code.

        Args:
            Regular cr, uid, ids

        Returns:
            dict {asset_id: code}
        """
        seq_model = self.pool.get('ir.sequence')
        assets = self.browse(cr, uid, ids)
        for asset in assets:
            cat_code = asset.category_id.code
            com_code = asset.company_id.code
            if not cat_code or not com_code:
                raise orm.except_orm('Error', """Problem generating the asset code.
                                        Please check the company code and the asset category code.""")
            if asset.category == 'scholarly':
                type_code = '02'
            elif asset.category == 'administrative':
                type_code = '01'
            else:
                type_code = '00'
            if asset.code:
                code = asset.code.split('-')
                code[1] = type_code
                code[2] = str(cat_code)
                code = '-'.join(code)
            else:
                try:
                    seq_id = seq_model.search(cr, uid, [('name', '=',
                        'Code {0}'.format(asset.company_id.name))])[0]
                    seq_number = seq_model.get_id(cr, uid, seq_id)
                    seq_number = str(seq_number)
                    seq_number = seq_number.lstrip()
                    code = "{0}-{1}-{2}-{3}".format(str(com_code), type_code,
                        str(cat_code), seq_number)
                except IndexError:
                    raise orm.except_orm('Error', """There is no sequence for the selected company.
                                         Please verify.""")
            return {asset.id: code}

    def get_period(self, cr, uid, id, context=None):
        """Retrieves the period corresponding to the passed depreciation
        line and returns its id."""
        period_obj = self.pool.get('account.period')
        depreciation_obj = self.pool.get('account.asset.depreciation.line')
        depre_date = depreciation_obj.browse(cr, uid, id,
                                             context).depreciation_date.split('-')
        period_id = period_obj.search(cr, uid,
                                      [('code', '=', '{0}/{1}'.format(depre_date[1], depre_date[0]))],
                                      limit=1)
        try:
            return period_id[0]
        except IndexError, e:
            return False

    def prepare_account_move(self, cr, uid, depreciation_line_id, period_id, context=None):
        """Setup values to create a new account move based in asset depreciation line

        Args:
            depreciation_line_id; int
            period_id; int

        Return:
            dictionary
            """
        asset_line_obj = self.pool.get('account.asset.depreciation.line')
        asset_line = asset_line_obj.browse(cr, uid, depreciation_line_id, context)
        asset_name = asset_line.name.encode('utf-8')
        res = {
            'name': asset_name,
            'period_id': period_id,
            'state': 'posted',
            'ref': asset_name,
            'date': date.today().isoformat(),
            'journal_id': asset_line.asset_id.category_id.journal_id.id,
            'company_id': asset_line.asset_id.company_id.id
        }
        return res

    def prepare_move_line(self, cr, uid, line_id, move_id, period_id,
                          move_type, context=None):
        """Returns the values to create an account move line.

        Args:
            line_id; depreciation line id
            move_id; parent account.move id
            type; string; debit or credit

        Returns:
            {field: value}
        """
        line_obj = self.pool.get('account.asset.depreciation.line')
        currency_obj = self.pool.get('res.currency')
        line = line_obj.browse(cr, uid, line_id, context)
        company_currency = line.asset_id.company_id.currency_id.id
        asset_currency = line.asset_id.currency_id.id
        amount = currency_obj.compute(cr, uid, asset_currency, company_currency,
                                      line.amount, context)
        sign = (line.asset_id.category_id.journal_id.type == 'purchase' and 1) or -1
        amount_currency = (company_currency != asset_currency and - sign *
                           line.amount or 0.0)
        if move_type == 'debit':
            debit, credit = amount, 0.0
            account = line.asset_id.category_id.account_depreciation_id.id
            asset = None
        else:
            debit, credit = 0.0, amount
            account = line.asset_id.category_id.account_expense_depreciation_id.id
            asset = line.asset_id.id
        values = {
            'name': line.asset_id.name.encode('utf-8'),
            'partner_id': line.asset_id.partner_id.id,
            #LOV Python
            'debit': debit and credit or credit,
            'credit': debit and credit or debit,
            'move_id': move_id,
            'ref': line.name.encode('utf-8'),
            'account_id': account,
            'journal_id': line.asset_id.category_id.journal_id.id,
            'currency_id': company_currency != asset_currency and asset_currency or False,
            'date': date.today().isoformat(),
            'amount_currency': amount_currency,
            'period_id': period_id,
            'asset_id': asset,
            'company_id': line.asset_id.company_id.id,
        }
        return values

    def get_asset_ids(self, cr, context=None):
        """Retrieve the assets using SQL for a better performance."""
        query = """SELECT id from {0} WHERE active = True and state like 'open' limit 25"""
        query = query.format(self._table)
        cr.execute(query)
        ids = [asset[0] for asset in cr.fetchall() if asset]
        return ids

    def run_asset_entry(self, cr, uid, context=None):
        #import pdb; pdb.set_trace()
        """Method that checks all lines in the model account asset
        deprecated and if the date is equal or greater than today it
        creates the account entry with the status settled.

        Args:
            cr, uid, ids, context

        Return:
            List of created account moves
        """

        logging.getLogger(self._name).info("Starting run_asset_entry cron job.")
        starting_point = time.time()

        account_move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        asset_obj = self.pool.get("account.asset.asset")
        asset_lines_obj = self.pool.get('account.asset.depreciation.line')
        today = date.today()
        asset = asset_obj.search(cr, uid, [('active','=',True), ('state','=','open')])

        import pdb; pdb.set_trace()
        for record in asset:

            try:
                asset_depreciation_lines = asset_lines_obj.search(cr, uid, [('asset_id','=', record), ('depreciation_date','<=',today.isoformat()), ('move_check','=', 0)], limit=1)
                asset_line = asset_lines_obj.browse(cr, uid, asset_depreciation_lines, context=context)
                asset_name = False
                if asset_line:
                    today = date.today()
                    if not asset_line.asset_id.name:
                        asset_name = 'Activo fijo sin nombre'
                    else:
                        asset_name = (asset_line.asset_id.name).encode('utf-8')

                    period_id = self.get_period(cr, uid, asset_line.id)

                    if not period_id:
                        company_name = asset_line.asset_id.company_id.name
                        logging.getLogger(self._name).error(
                            """No period found for the date {0}
                            and company {1}""".format(asset_line.depreciation_date, company_name[1]))
                        break
                    try:
                        values = self.prepare_account_move(cr, uid, asset_line.id, period_id, context)
                        created_id = account_move_obj.create(cr, uid, values, context)
                        logging.getLogger(self._name).info("""account.move created for {0}""".format(asset_name))
                    except:
                        logging.getLogger(self._name).error("Error creating account move {0}".format(asset_name))
                        raise orm.except_orm('Error', "Failure creating the account move object.")
                    try:
                        debit_values = self.prepare_move_line(cr, uid, asset_line.id, created_id, period_id, 'debit')
                        credit_values = self.prepare_move_line(cr, uid, asset_line.id, created_id, period_id, 'credit')
                        move_line_obj.create(cr, uid, debit_values, context)
                        move_line_obj.create(cr, uid, credit_values, context)
                        asset_lines_obj.write(cr, uid, asset_line.id, {'move_check': True, 'move_id': created_id})
                        logging.getLogger(self._name).info("""account.move.line created for {0}""".format(asset_name))
                    except:
                        logging.getLogger('account.asset.asset').error(
                            """ERROR creating the entries of
                            account move from {0}.""".format(__name__))
                        raise orm.except_orm('Error', 'Failure creating the'
                            ' account move lines.')

            except:
                logging.getLogger(self._name).error("This script stop trying to create a move for asset {0}!!! Please check".format(asset_name))
                raise orm.except_orm('Error', "Run asset entries finish unsusccesfully.")

        elapsed_time = time.time() - starting_point
        elapsed_time_int = int(elapsed_time)
        elapsed_time_minutes = elapsed_time_int / 60
        elapsed_time_seconds = elapsed_time_int % 60

        logging.getLogger(self._name).info("Run asset entries completed succesfully!")
        _logger.info('This task has been complete in %s minutos y %s segundos'
                                 %(elapsed_time_minutes, elapsed_time_seconds))

    # def run_asset_entry(self, cr, uid, context=None):
    #     #import pdb; pdb.set_trace()
    #     """Method that checks all lines in the model account asset
    #     deprecated and if the date is equal or greater than today it
    #     creates the account entry with the status settled.
    #
    #     Args:
    #         cr, uid, ids, context
    #
    #     Return:
    #         List of created account moves
    #     """
    #
    #     logging.getLogger(self._name).info("Starting run_asset_entry cron job.")
    #     account_move_obj = self.pool.get('account.move')
    #     move_line_obj = self.pool.get('account.move.line')
    #     asset_lines_obj = self.pool.get('account.asset.depreciation.line')
    #     ids = self.get_asset_ids(cr)
    #
    #     counter = 0
    #     import pdb; pdb.set_trace()
    #     for asset in ids:
    #
    #         asset = self.read(cr, uid, asset, context=context)
    #
    #         for asset_line in asset.get('depreciation_line_ids'):
    #
    #             today = date.today()
    #             asset_name = asset.get('name').encode('utf-8')
    #             asset_line = asset_lines_obj.read(cr, uid, asset_line)
    #
    #             if asset_line.get('depreciation_date') <= today.isoformat() and not asset_line.get('move_check'):
    #                 period_id = self.get_period(cr, uid, asset_line.get('id'))
    #
    #                 if not period_id:
    #                     company_name = asset.get('company_id')
    #                     logging.getLogger(self._name).error(
    #                         """No period found for the date {0}
    #                         and company {1}""".format(asset_line.get('depreciation_date'), company_name[1]))
    #                     break
    #                 try:
    #                     values = self.prepare_account_move(cr, uid, asset_line.get('id'), period_id, context)
    #                     created_id = account_move_obj.create(cr, uid, values, context)
    #                     logging.getLogger(self._name).info("""account.move created for {0}""".format(asset_name))
    #                 except:
    #                     logging.getLogger(self._name).error("Error creating account move {0}".format(asset_name))
    #                     raise orm.except_orm('Error', "Failure creating the account move object.")
    #                 try:
    #                     debit_values = self.prepare_move_line(cr, uid, asset_line.get('id'), created_id, period_id, 'debit')
    #                     credit_values = self.prepare_move_line(cr, uid, asset_line.get('id'), created_id, period_id, 'credit')
    #                     move_line_obj.create(cr, uid, debit_values, context)
    #                     move_line_obj.create(cr, uid, credit_values, context)
    #                     asset_lines_obj.write(cr, uid, asset_line.get('id'), {'move_check': True, 'move_id': created_id})
    #                     logging.getLogger(self._name).info("""account.move.line created for {0}""".format(asset_name))
    #                 except:
    #                     logging.getLogger('account.asset.asset').error(
    #                         """ERROR creating the entries of
    #                         account move from {0}.""".format(__name__))
    #                     raise orm.except_orm('Error', 'Failure creating the'
    #                         ' account move lines.')
    #
    #             #else:
    #             #    logging.getLogger(self._name).info("Este activo ya esta asentado!")


    _columns = {
    'department_id' : fields.many2one('hr.department', 'Departament'),
    'life_expectancy' : fields.float('Life Expectancy', help="""Life expectancy
     of the asset in years."""),
    'life_expectancy_percentage': fields.float('Life Expectancy Percentage'),
    'stage_id': fields.many2one('account.asset.stage', 'Stage',
        help="""The stage of the asset indicate in wich point of his life is
        at the moment. You can add new stages in configuration."""),
    'code': fields.char("Code", size=9, required=True),
    'model_id': fields.many2one('account.asset.model', 'Model'),
    'brand_id': fields.related('model_id', 'brand_id', string='Brand',
        type="many2one", relation="account.asset.model", readonly=True),
    'category': fields.selection((
        ('administrative', 'Administrative'),
        ('scholarly', 'Scholarly'),
        ('none', 'None')), 'Type of asset', help="""The type of
    asset, scholarly or administrative."""),
    'asset_move_ids': fields.one2many('account.asset.move', 'asset_id',
        'Movements')
    }
    _defaults = {
    'category': 'administrative',
    }

class AccountCategory(orm.Model):

    _name = 'account.asset.category'
    _inherit ='account.asset.category'
    _auto = True
    _columns ={
    'code' : fields.char('Code', size=4, required=True),

    }

class ResCompany(orm.Model):

    _name = 'res.company'
    _inherit = 'res.company'
    _auto = True
    _columns ={
    'code' : fields.char('Code', size=4, required=True),

    }


class AssetBrand(orm.Model):

    _name = 'account.asset.brand'
    _auto = True
    _columns = {
    'name': fields.char('Asset brand', required=True, size=64)
    }


class AssetModel(orm.Model):

    _name = 'account.asset.model'
    _auto = True
    _columns = {
    'name': fields.char('Asset model', required=True, size=64),
    'brand_id': fields.many2one('account.asset.model', 'Brand')
    }

class AssetStages(orm.Model):

    _name = 'account.asset.stage'
    _auto = True
    _columns = {
    'name': fields.char('Name', size=32, required=True),
    'description': fields.char('Description', size=128)
    }
