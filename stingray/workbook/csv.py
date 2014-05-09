#!/usr/bin/env python3

# .. _`workbook_csv`:
#
#
# CSV Workbook
# ---------------
#
# ::

import csv
import logging
import pprint

from stingray.workbook.base import Workbook
import stingray.sheet
import stingray.cell

# ..  py:module:: workbook
#
# ..  py:class:: CSV_Workbook
#
# We're wrapping the :py:func:`csv.reader`.  We need to create proper
# :py:class:`cell.TextCell` instances instead of the default string values
# that :py:mod:`csv` normally creates.
#
# ::

class CSV_Workbook( Workbook ):
    """Uses ``csv.reader``.  There's one sheet only."""
    def __init__( self, name, file_object=None, **kw ):
        """Prepare the workbook for reading.
        :param name: File name
        :param file_object: Optional file-like object.  If omitted, the named file is opened.
            If provided, it must be opened with  newline='' to permit non-standard
            line-endings.

        The kw are passed to :py:func:`csv.reader`
        to provide dialect information."""
        super().__init__( name, file_object )
        if self.file_obj:
            self.the_file= None
            self.rdr= csv.reader( self.file_obj, **kw )
        else:
            self.the_file = open( name, 'r', newline='' )
            self.rdr= csv.reader( self.the_file, **kw )

# We can build an eager :py:class:`sheet.Row` or a :py:class:`sheet.LazyRow` from
# the available data.
# The eager Row includes the conversions.  The :py:class:`sheet.LazyRow` defers
# the conversions until the callback to :py:meth:`workbook.Workbook.row_get`.
#
# ..  py:method:: CSV_Workbook.rows_of( sheet )
#
# ::

    def rows_of( self, sheet ):
        """An iterator over all rows of the named sheet.
        For CSV files, the sheet.name is simply ignored.
        """
        for data in self.rdr:
            logging.debug( pprint.pformat( data, indent=4 ) )
            row = stingray.sheet.Row( sheet, *(stingray.cell.TextCell(col,self) for col in data) )
            yield row

# ..  py:method:: CSV_Workbook.row_get( row, attribute )
#
# ::

    def row_get( self, row, attribute ):
        """Create a Cell from the row's data."""
        return row[attribute.position]

# Since :py:mod:`csv` is eager, returning an individual :py:class:`cell.TextCell`
# is easy.
