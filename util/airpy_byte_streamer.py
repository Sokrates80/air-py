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

    def _use_usb(self, stream):
        """
        Writes the stream to usb
        :param stream: byte stream
        :return:
        """
        self.__USB.write(stream)

    def _use_wifi(self, stream):
        """
        Writes the stream to wifi
        :param stream: byte stream
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
            self._use_usb(bytearray(bytes))
        elif self.__TRANSPORT == STREAM_VIA_WIFI:
            self._use_wifi(bytearray(bytes))