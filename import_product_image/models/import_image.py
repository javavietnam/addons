# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Saritha Sahadevan (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
import csv
import urllib
import base64
from io import StringIO
import sys
from odoo import models, fields, api
import os
import ctypes
from PIL import Image
from io import BytesIO
import requests
from binascii import a2b_base64
from odoo.exceptions import UserError, ValidationError
from odoo.tools import frozendict, image_to_base64, hex_to_rgb
class ProductImageImportWizard(models.TransientModel):
    _name = 'import.product_image'

    product_model = fields.Selection([('1', 'Product Template'), ('2', 'Product Variants')], string="Product Model")
    pdt_operation = fields.Selection([('1', 'Product Creation'), ('2', 'Product Updation')], string="Product Operation")
    file = fields.Binary('File to import', required=True)

    def loadImages(self,path):
        # return array of images

        img = Image.open(path)
        return img

    def import_file(self):
        file =  a2b_base64(self.file).decode('latin-1').encode("utf-8")
        file_string = file.decode("utf-8")
        file_string = file_string.split('\n')
        reader = csv.reader(file_string, delimiter=',')
        csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))
        skip_header = True
        for row in reader:
            if skip_header:
                skip_header = False
                continue
            if len(row)>0:
                product = row[0]
                image_path = row[1]
                if "http://" in image_path or "https://" in image_path:
                    try:
                        # link = urllib.request.urlopen(image_path).read()
                        # image_base64 = base64.encodestring(link)
                        image_base64 = base64.b64encode(requests.get(image_path).content)
                        if self.product_model == '1':
                            product_obj = self.env['product.template']
                        else:
                            product_obj = self.env['product.product']
                        product_id = product_obj.search([('name', '=', product)])

                        vals = {
                            'image_1920': image_base64,
                            'name': product,
                        }
                        if self.pdt_operation == '1' and not product_id:
                            product_obj.create(vals)
                        elif self.pdt_operation == '1' and product_id:
                            product_id.write(vals)
                        elif self.pdt_operation == '2' and product_id:
                            product_id.write(vals)
                        elif not product_id and self.pdt_operation == '2':
                            raise UserError("Could not find the product '%s'" % product)
                    except Exception as e:
                        # raise UserError("Please provide correct URL for product '%s' or check your image size.!" % product)
                        print(e)
                else:
                    try:
                        with self.loadImages(image_path) as image:
                            # a = base64.b64encode(image.read())
                            # im = Image.open(BytesIO(base64.b64decode(a)))
                            # image_base64 = image.read().encode("base64")
                            if self.product_model == '1':
                                product_obj = self.env['product.template']
                            else:
                                product_obj = self.env['product.product']
                            product_id = product_obj.search([('name', '=', product)])
                            vals = {
                                'image_1920':image_to_base64(image.convert("RGB"),image.format),
                                'name': product,
                            }
                            if self.pdt_operation == '1' and not product_id:
                                product_obj.create(vals)
                            elif self.pdt_operation == '1' and product_id:
                                product_id.write(vals)
                            elif self.pdt_operation == '2' and product_id:
                                product_id.write(vals)
                            elif not product_id and self.pdt_operation == '2':
                                raise UserError("Could not find the product '%s'" % product)
                    except IOError:
                        raise UserError("Could not find the image '%s' - please make sure it is accessible to this script" %
                                    product)

