#!/usr/bin/env python
# -*- coding: utf-8 -*-

test = DatabaseModel('test')
columns = ColumnsDatabase()

columns.insert_column('col1','varchar(50)')
columns.insert_column('col2','text')
columns.insert_column('col3','integer')

test.create_table('prueba',columns)
test.create_table('ejemplo',columns)

rows = RowsDatabase(int(test.num_columns_table('prueba')))
rows.insert_value(('fila1','mas texto',200))
rows.insert_value(('fila2','menos texto',160))

col = ColumnsDatabase()
col.insert_column('col4','tinyint')

test.alter_table_column('prueba',col)

test.insert_row('prueba', rows)

#test.delete_row('prueba', 'col1', 'fila1')

#test.update_row('prueba', 'col4', 'gatitos', 'col2', 'fila2')

test.close_db()
