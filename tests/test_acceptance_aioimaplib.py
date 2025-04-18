# -*- coding: utf-8 -*-
#    aioimaplib : an IMAPrev4 lib using python asyncio
#    Copyright (C) 2016  Bruno Thomas
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
import asyncio
import email

import os

import pytest

from aioimaplib.imap_testing_server import Mail
from tests.server_fixture import with_server, login_user_async


@pytest.mark.asyncio()
async def test_file_with_attachment(with_server):
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data/test_attachment.eml'), mode='br') as msg:
        imap_client = await login_user_async('user@mail', 'pass', select=True)
        mail = Mail(email.message_from_binary_file(msg))

        with_server.receive(mail, imap_user='user@mail')

        result, data = await imap_client.fetch('1', '(RFC822)')

        assert 'OK' == result
        assert [b'1 FETCH (RFC822 {418898}', mail.as_bytes(), b')', b'FETCH completed.'] == data
