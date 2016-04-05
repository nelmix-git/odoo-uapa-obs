# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 18:23:26 2013

@author: Carlos Llamacho
"""
from openerp.osv import fields, orm


class books_authors(orm.Model):
    _name='books.authors'

    _columns = {
    'code': fields.integer('Book Code', size=16, required=True),
    'name': fields.char('Author Name', size=128, required=True)
    }

books_authors()


class book_editors(orm.Model):
    _name ='book.editors'

    _columns={
        'code': fields.integer('Editor code', size=16, required=True),
        'name': fields.char('Editor name', size=128, required=True)
        }

book_editors()


class product_product(orm.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    _columns = {
    'is_book': fields.boolean('Is Book'),
    'book_author_id': fields.many2one('books.authors', 'Book Authors'),
    'editorials_id': fields.many2one('book.editors', 'Editorials'),
    }

product_product()
