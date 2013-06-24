#!/usr/bin/env python
# FormatSMVADSCSN926.py
#   Copyright (C) 2011 Diamond Light Source, Graeme Winter
#
#   This code is distributed under the BSD license, a copy of which is
#   included in the root directory of this package.
#
# An implementation of the SMV image reader for ADSC images. Inherits from
# FormatSMVADSC, customised for beamline 8.3.1 at the ALS where people use
# two-theta offsets in the vertical direction.

from __future__ import division
from __future__ import print_function

from dxtbx.format.FormatSMVADSCSN import FormatSMVADSCSN


class FormatSMVADSCSN926(FormatSMVADSCSN):
    """A class for reading SMV format ADSC images, and correctly constructing
    a model for the experiment from this, for instrument number 926."""

    @staticmethod
    def understand(image_file):
        """Check to see if this is ADSC SN 926."""

        # check this is detector serial number 926

        size, header = FormatSMVADSCSN.get_smv_header(image_file)

        if int(header["DETECTOR_SN"]) != 926:
            return False

        return True

    def __init__(self, image_file):
        """Initialise the image structure from the given file, including a
        proper model of the experiment."""

        assert self.understand(image_file)

        FormatSMVADSCSN.__init__(self, image_file)

        return

    def _detector(self):
        """Return a model for a simple detector, allowing for the installation
        on on a two-theta stage. Assert that the beam centre is provided in
        the Mosflm coordinate frame."""

        distance = float(self._header_dictionary["DISTANCE"])
        beam_x = float(self._header_dictionary["BEAM_CENTER_X"])
        beam_y = float(self._header_dictionary["BEAM_CENTER_Y"])
        pixel_size = float(self._header_dictionary["PIXEL_SIZE"])
        image_size = (
            float(self._header_dictionary["SIZE1"]),
            float(self._header_dictionary["SIZE2"]),
        )
        two_theta = float(self._header_dictionary["TWOTHETA"])
        overload = 65535
        underload = 0

        return self._detector_factory.two_theta(
            "CCD",
            distance,
            (beam_y, beam_x),
            "+x",
            "-y",
            "+x",
            two_theta,
            (pixel_size, pixel_size),
            image_size,
            (underload, overload),
            [],
        )


if __name__ == "__main__":

    import sys

    for arg in sys.argv[1:]:
        print(FormatSMVADSC.understand(arg))
