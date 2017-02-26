from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import StatementLine
from ofxstatement.exceptions import ParseError
import csv


LINELENGTH = 7
HEADER_START = "Volgnummer"

class FintroBePlugin(Plugin):
    """Belgian Fintro Bank plugin for ofxstatement
    """

    def get_parser(self, filename):
        f = open(filename, 'r')
        parser = FintroBeParser(f)
        return parser


class FintroBeParser(CsvStatementParser):

    date_format = "%d/%m/%Y"

	# Header looks like Volgnummer;Uitvoeringsdatum;Valutadatum;Bedrag;Valuta rekening;Details;Rekeningnummer

    mappings = {
    	'refnum': 0,
        'memo': 5,
        'date': 1,
        'amount': 3,
    }

    account_id_index = 6
    currency_index = 4

    line_nr = 0

    def parse_float(self, value):
        """Return a float from a string with ',' as decimal mark.
        """
        return float(value.replace('.','').replace(',','.'))

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        return csv.reader(self.fin, delimiter=';')

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        self.line_nr += 1
        if line[0] == HEADER_START:
            return None
        elif len(line) != LINELENGTH:
            raise ParseError(self.line_nr,
                             'Wrong number of fields in line! ' +
                             'Found ' + str(len(line)) + ' fields ' +
                             'but should be ' + str(LINELENGTH) + '!')

        # Check the account id. Each line should be for the same account!
        if self.statement.account_id:
            if line[self.account_id_index] != self.statement.account_id:
                raise ParseError(self.line_nr,
                                 'AccountID does not match on all lines! ' +
                                 'Line has ' + line[0] + ' but file ' +
                                 'started with ' + self.statement.account_id)
        else:
            self.statement.account_id = line[self.account_id_index]

        # Check the currency. Each line should be for the same currency!
        if self.statement.currency:
            if line[self.currency_index] != self.statement.currency:
                raise ParseError(self.line_nr,
                                 'Currency does not match on all lines! ' +
                                 'Line has ' + line[3] + ' but file ' +
                                 'started with ' + self.statement.currency)
        else:
            self.statement.currency = line[self.currency_index]


        stmt_ln = super(FintroBeParser, self).parse_record(line)

        return stmt_ln
