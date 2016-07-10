"""
airPy is a flight controller based on pyboard and written in micropython.

The MIT License (MIT)
Copyright (c) 2016 Cristian Maugeri, filla.one@gmail.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""


import pyb


STREAM_VIA_USB = 0
STREAM_VIA_WIFI = 1


class airpy_byte_streamer:

    def __init__(self):
        """
        Byte streamer entry point
        :return:
        """
        self.__TRANSPORT = STREAM_VIA_USB
        self.__USB = pyb.USB_VCP()

    def set_transport(self, transport):
        """
        Changes transport
        :param transport: layer to be used
        :return:
        """
        self.__TRANSPORT = transport

    def _use_usb_write(self, stream):
        """
        Writes the stream to usb
        :param stream: byte stream
        :return:
        """
        self.__USB.write(stream)

    def _use_usb_read(self):
        """
        Read one byte from usb
        :return: 1 read byte
        """
        return self.__USB.read(1)

    def _use_wifi_write(self, stream):
        """
        Writes the stream to wifi
        :param stream: byte stream
        :return:
        """
        pass

    def _use_wifi_read(self):
        """
        Read the stream from wifi
        :return:
        """
        pass

    def stream_byte(self, bytes):
        """
        Stream bytes using selected protocol
        :param bytes: bytes to stream
        :return:
        """
        if self.__TRANSPORT == STREAM_VIA_USB:
            self._use_usb_write(bytearray(bytes))
        elif self.__TRANSPORT == STREAM_VIA_WIFI:
            self._use_wifi_write(bytearray(bytes))

    def read_byte(self):
        """
        Stream bytes using selected protocol
        :return: bytes from the stream
        """
        if self.__TRANSPORT == STREAM_VIA_USB:
            return self._use_usb_read()
        elif self.__TRANSPORT == STREAM_VIA_WIFI:
            return self._use_wifi_read()
