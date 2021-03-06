#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Rotate class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.blockmodel import BlockModel


class Rotate(BlockModel):
    """
    This class contains methods related the Rotate class.
    """
    # -------------------------------------------------------------------------

    def __init__(self):
        BlockModel.__init__(self)

        self.language = "c"
        self.framework = "opencv"

        # Appearance
        self.help = "Adiciona bordas na imagem."
        self.label = "Rotate Image"
        self.color = "90:5:10:150"
        self.group = "Experimental"
        self.ports = [{"type":"mosaicode_lib_c_opencv.extensions.ports.image",
                       "name":"input_image",
                       "label":"Input Image",
                       "conn_type":"Input"},
                      {"type":"mosaicode_lib_c_opencv.extensions.ports.double",
                       "name":"angle",
                       "label":"Angle",
                       "conn_type":"Input"},
                      {"type":"mosaicode_lib_c_opencv.extensions.ports.image",
                       "name":"output_image",
                       "label":"Output Image",
                       "conn_type":"Output"}]

        self.properties = [{"name": "isCenter",
                            "label": "Use Image Center",
                            "type": MOSAICODE_CHECK
                            },
                           {"name": "isScalling",
                            "label": "Resize Image To Fit In",
                            "type": MOSAICODE_CHECK
                            },
                           {"name": "isFilling",
                            "label": "Fill Leftovers",
                            "type": MOSAICODE_CHECK
                            },
                           {"name": "x",
                            "label": "Point x",
                            "type": MOSAICODE_INT,
                            "value": 20,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "y",
                            "label": "Point y",
                            "value": 20,
                            "type": MOSAICODE_INT,
                            "lower": 0,
                            "upper": 65535,
                            "step": 1
                            },
                           {"name": "angle",
                            "label": "Angle",
                            "type": MOSAICODE_FLOAT,
                            "lower": 0,
                            "upper": 360,
                            "step": 1
                            }
                           ]

        # -------------------C/OpenCv code------------------------------------
        self.codes["declaration"] = \
            'IplImage * $port[input_image]$ = NULL;\n' + \
            'double $port[angle]$ = $prop[angle]$;\n' + \
            'IplImage * $port[output_image]$ = NULL;\n'

        self.codes["function"] = \
            "#define PI 3.1415926535898\n" + \
            "double rads(double degs){\n" + \
            "   return (PI/180 * degs);\n" + \
            "}\n\n"

    # ----------------------------------------------------------------------
    def generate_function_call(self):
        value = \
            '\n if($port[input_image]$)\n  {\n' + \
            '       double scale;\n int H;\n    int W;\n' + \
            '       W = $port[input_image]$->width;\n' + \
            '       H = $port[input_image]$->height;\n' + \
            '       $port[output_image]$ = cvCreateImage(cvSize(W,H),' + \
            '       $port[input_image]$->depth,$port[input_image]$->nChannels);\n' + \
            '       CvMat* mat = cvCreateMat(2,3,CV_32FC1);\n'
        if self.isCenter == "true":
            value += '      CvPoint2D32f center = cvPoint2D32f(W/2, H/2);\n'
        else:
            value += '      CvPoint2D32f center = cvPoint2D32f($prop[x]$, $prop[y]$);\n'

        if self.isScalling == "true":
            value += '      scale = H/(fabs(H*sin(rads' + \
                '(90-abs($port[angle]$)))) + ' + \
                'fabs(W*sin(rads(abs($port[angle]$)))));\n' + \
                '       cv2DRotationMatrix' + \
                '(center,$port[angle]$,scale,mat);\n'
        else:
            value += '      cv2DRotationMatrix' + \
                '(center,$port[angle]$,1.0,mat);\n'

        if self.isFilling == "true":
            value += '      cvWarpAffine($port[input_image]$, ' + \
                '$port[output_image]$, mat, ' + \
                'CV_WARP_FILL_OUTLIERS, cvScalarAll(0));\n'
        else:
            value += '      cvWarpAffine($port[input_image]$,' + \
                '$port[output_image]$,mat,0,cvScalarAll(0));\n'

        value += '  }\n'
        return value
# -----------------------------------------------------------------------------
