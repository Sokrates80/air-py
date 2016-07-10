from aplink.messages.ap_save_tx_calibration import SaveTxCalibration
#from utils.airpy_config_utils import load_config_file, save_config_file

test_payload = bytearray([0,0,0,172,0,0,0,172,0,0,0,172,0,0,0,172,
                        0,0,6,255,0,0,6,255,0,0,6,255,0,0,6,255,
                        0,0,2,255,0,0,2,255,0,0,2,255,0,0,2,255])


# TEST 1 - Packet Decoding
result = SaveTxCalibration.decode_payload(test_payload)

print("Results: {}".format(result))

#cm = load_config_file("config.json")
#cm['rcRadio']['channels_min'] = result[0]
#cm['rcRadio']['channels_max'] = result[1]
#cm['rcRadio']['channels_center'] = result[2]
#save_config_file("config.json", cm)
#print("Done")

