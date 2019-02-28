import os
import base

import core.utilities.colour as c

class BuilderNabojVenue(base.BuilderNaboj):
    target = 'venue'
    subdir = 'venues'

    def __init__(self):
        self.rootContextClass = base.ContextTearoff
        self.templates = {
            'templates': ['barcodes.txt', 'tearoff.tex', 'envelope.tex'],
        }
        super().__init__()

    def createArgParser(self):
        super().createArgParser()
        self.parser.add_argument('-p', '--venue', type = str)

    def id(self):
        return (self.args.competition, self.args.volume, self.args.venue)

    def path(self):
        return (self.args.competition, '{:02d}'.format(self.args.volume), self.subdir, self.args.venue)


BuilderNabojVenue().build()
