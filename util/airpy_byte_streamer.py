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
        Read the stream from usb
        :return: byte stream
        """
        return self.__USB.readall()

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
