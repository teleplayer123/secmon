import ctypes as ct
from ctypes.wintypes import DWORD, HANDLE, ULONG, BOOLEAN, UINT
from enum import Enum
import struct


ERROR_SUCCESS = 0
UINT32 = ct.c_uint32
UINT16 = ct.c_uint16
UINT8 = ct.c_uint8

class WLAN_CONNECTION_MODE(Enum):
    wlan_connection_mode_profile = 0,
    wlan_connection_mode_temporary_profile = 1
    wlan_connection_mode_discovery_secure = 2
    wlan_connection_mode_discovery_unsecure = 3
    wlan_connection_mode_auto = 4
    wlan_connection_mode_invalid = 5

class WLAN_INTF_OPCODE(Enum):
    wlan_intf_opcode_autoconf_start = 0
    wlan_intf_opcode_autoconf_enabled = 1
    wlan_intf_opcode_background_scan_enabled = 2
    wlan_intf_opcode_media_streaming_mode = 3
    wlan_intf_opcode_radio_state = 4
    wlan_intf_opcode_bss_type = 5
    wlan_intf_opcode_interface_state = 6
    wlan_intf_opcode_current_connection = 7
    wlan_intf_opcode_channel_number = 8
    wlan_intf_opcode_supported_infrastructure_auth_cipher_pairs = 9
    wlan_intf_opcode_supported_adhoc_auth_cipher_pairs = 10
    wlan_intf_opcode_supported_country_or_region_string_list = 11
    wlan_intf_opcode_current_operation_mode = 12
    wlan_intf_opcode_supported_safe_mode = 13
    wlan_intf_opcode_certified_safe_mode = 14
    wlan_intf_opcode_hosted_network_capable = 15
    wlan_intf_opcode_management_frame_protection_capable = 16
    wlan_intf_opcode_secondary_sta_interfaces = 17
    wlan_intf_opcode_secondary_sta_synchronized_connections = 18
    wlan_intf_opcode_autoconf_end = 0x0fffffff
    wlan_intf_opcode_msm_start = 0x10000100
    wlan_intf_opcode_statistics = 0x10000101
    wlan_intf_opcode_rssi = 0x10000102
    wlan_intf_opcode_msm_end = 0x1fffffff
    wlan_intf_opcode_security_start = 0x20010000
    wlan_intf_opcode_security_end = 0x2fffffff
    wlan_intf_opcode_ihv_start = 0x30000000
    wlan_intf_opcode_ihv_end = 0x3fffffff

DOT11_AUTH_ALGORITHM_T = UINT
class DOT11_AUTH_ALGORITHM(Enum):
    DOT11_AUTH_ALGO_80211_OPEN = 1
    DOT11_AUTH_ALGO_80211_SHARED_KEY = 2
    DOT11_AUTH_ALGO_WPA = 3
    DOT11_AUTH_ALGO_WPA_PSK = 4
    DOT11_AUTH_ALGO_WPA_NONE = 5
    DOT11_AUTH_ALGO_RSNA = 6
    DOT11_AUTH_ALGO_RSNA_PSK = 7
    DOT11_AUTH_ALGO_WPA3 = 8
    DOT11_AUTH_ALGO_WPA3_ENT_192 = DOT11_AUTH_ALGO_WPA3
    DOT11_AUTH_ALGO_WPA3_SAE = 9
    DOT11_AUTH_ALGO_OWE = 10
    DOT11_AUTH_ALGO_WPA3_ENT = 11
    DOT11_AUTH_ALGO_IHV_START = 0x80000000
    DOT11_AUTH_ALGO_IHV_END = 0xffffffff

DOT11_CIPHER_ALGORITHM_T = UINT
class DOT11_CIPHER_ALGORITHM(Enum):
    DOT11_CIPHER_ALGO_NONE = 0x00
    DOT11_CIPHER_ALGO_WEP40 = 0x01
    DOT11_CIPHER_ALGO_TKIP = 0x02
    DOT11_CIPHER_ALGO_CCMP = 0x04
    DOT11_CIPHER_ALGO_WEP104 = 0x05
    DOT11_CIPHER_ALGO_BIP = 0x06
    DOT11_CIPHER_ALGO_GCMP = 0x08
    DOT11_CIPHER_ALGO_GCMP_256 = 0x09
    DOT11_CIPHER_ALGO_CCMP_256 = 0x0a
    DOT11_CIPHER_ALGO_BIP_GMAC_128 = 0x0b
    DOT11_CIPHER_ALGO_BIP_GMAC_256 = 0x0c
    DOT11_CIPHER_ALGO_BIP_CMAC_256 = 0x0d
    DOT11_CIPHER_ALGO_WPA_USE_GROUP = 0x100
    DOT11_CIPHER_ALGO_RSN_USE_GROUP = 0x100
    DOT11_CIPHER_ALGO_WEP = 0x101
    DOT11_CIPHER_ALGO_IHV_START = 0x80000000
    DOT11_CIPHER_ALGO_IHV_END = 0xffffffff

MAX_SIMULTANEOUS_BAND_CONNECTIONS_ALLOWED = 4

WDI_BAND_ID_T = UINT32
class WDI_BAND_ID(Enum):
    WDI_BAND_ID_UNKNOWN = 0
    WDI_BAND_ID_2400 = 1
    WDI_BAND_ID_5000 = 2
    WDI_BAND_ID_60000 = 3
    WDI_BAND_ID_900 = 4
    WDI_BAND_ID_6000 = 6
    WDI_BAND_ID_IHV_CUSTOM_START = 0x80000000
    WDI_BAND_ID_IHV_CUSTOM_END = 0x81000000
    WDI_BAND_ID_ANY = 0xFFFFFFFF

RSNA_OUI_PREFIX = 0x205

AKM_FROM_TYPE = lambda p,a: int("{:04x}{:02x}".format(p, a), 16)
RSNA_AKM_SUITE_T = UINT32
class RSNA_AKM_SUITE(Enum):
    rsna_akm_none = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 0),
    rsna_akm_1x = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 1),
    rsna_akm_psk = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 2),
    rsna_akm_ft_1x_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 3),
    rsna_akm_ft_psk_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 4),
    rsna_akm_1x_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 5),
    rsna_akm_psk_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 6),
    rsna_akm_tdls_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 7),
    rsna_akm_sae_pmk256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 8),
    rsna_akm_ft_sae_pmk256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 9),
    rsna_akm_peerkey_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 10),
    rsna_akm_1x_suite_b_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 11),
    rsna_akm_1x_suite_b_sha384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 12),
    rsna_akm_ft_1x_sha384_cmp_256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 13),
    rsna_akm_fils_1x_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 14),
    rsna_akm_fils_1x_sha384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 15),
    rsna_akm_ft_fils_1x_sha256 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 16),
    rsna_akm_ft_fils_sha384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 17),
    rsna_akm_owe = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 18),
    rsna_akm_ft_psk_sha384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 19),
    rsna_akm_psk_sha384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 20),
    rsna_akm_ft_1x_sha384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 22),
    rsna_akm_1x_sha384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 23),
    rsna_akm_sae_pmk384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 24),
    rsna_akm_ft_sae_pmk384 = AKM_FROM_TYPE(RSNA_OUI_PREFIX, 25),
    rsna_akm_max = rsna_akm_ft_sae_pmk384

class DOT11_AUTH_CIPHER_PAIR(ct.Structure):

    _fields_ = [
        ("AuthAlgoId", DOT11_AUTH_ALGORITHM_T),
        ("CipherAlgoId", DOT11_CIPHER_ALGORITHM_T)
    ]

class WIFI_STA_BANDS_COMBINATION(ct.Structure):

    _fields_ = [
        ("NumStaBands", UINT8),
        ("BandIDs", WDI_BAND_ID_T * MAX_SIMULTANEOUS_BAND_CONNECTIONS_ALLOWED)
    ]

class WDI_MAC_ADDRESS(ct.Structure):

    _fields_ = [
        ("Address", UINT8 * 6)
    ]

WDI_CIPHER_ALGORITHM_T = UINT
class WDI_CIPHER_ALGORITHM(Enum):
    DOT11_CIPHER_ALGO_NONE = 0x00
    DOT11_CIPHER_ALGO_WEP40 = 0x01
    DOT11_CIPHER_ALGO_TKIP = 0x02
    DOT11_CIPHER_ALGO_CCMP = 0x04
    DOT11_CIPHER_ALGO_WEP104 = 0x05
    DOT11_CIPHER_ALGO_BIP = 0x06
    DOT11_CIPHER_ALGO_GCMP = 0x08
    DOT11_CIPHER_ALGO_GCMP_256 = 0x09
    DOT11_CIPHER_ALGO_CCMP_256 = 0x0a
    DOT11_CIPHER_ALGO_BIP_GMAC_128 = 0x0b
    DOT11_CIPHER_ALGO_BIP_GMAC_256 = 0x0c
    DOT11_CIPHER_ALGO_BIP_CMAC_256 = 0x0d
    DOT11_CIPHER_ALGO_WPA_USE_GROUP = 0x100
    DOT11_CIPHER_ALGO_RSN_USE_GROUP = 0x100
    DOT11_CIPHER_ALGO_WEP = 0x101
    DOT11_CIPHER_ALGO_IHV_START = 0x80000000
    DOT11_CIPHER_ALGO_IHV_END = 0xffffffff


class WIFI_STATION_CAPABILITIES(ct.Structure):

    """
    Call WIFI_STATION_CAPABILITIES_INIT to initialize this structure and fill in its Size field. 
    Then call WifiDeviceSetStationCapabilities to report station capabilities to WiFiCx.
    """

    _fields_ = [
        ("Size", ULONG),
        ("ScanSSIDListSize", UINT32),
        ("DesiredSSIDListSize", UINT32),
        ("PrivacyExemptionListSize", UINT32),
        ("KeyMappingTableSize", UINT32),
        ("DefaultKeyTableSize", UINT32),
        ("WEPKeyValueMaxLength", UINT32),
        ("MaxNumPerSTA", UINT32),
        ("SupportedQOSFlags", UINT8),
        ("HostFIPSModeImplemented", UINT8),
        ("MFPCapable", UINT8),
        ("AutoPowerSaveMode", BOOLEAN),
        ("BSSListCachemanagement", BOOLEAN),
        ("ConnectBSSSelectionOverride", BOOLEAN),
        ("MaxNetworkOffloadListSize", UINT32),
        ("HESSIDConnectionSupported", BOOLEAN),
        ("FTMAsInitiatorSupport", BOOLEAN),
        ("FTMNumberOfSupportedTargets", UINT32),
        ("HostWPA3FIPSModeEnabled_Deprecated", BOOLEAN),
        ("NumSupportedUnicastAlgorithms", ULONG),
        ("UnicastAlgorithmsList", DOT11_AUTH_CIPHER_PAIR),
        ("NumSupportedMulticastDataAlgorithms", ULONG),
        ("MulticastDataAlgorithmsList", DOT11_AUTH_CIPHER_PAIR),
        ("NumSupportedMulticastMgmtAlgorithms", ULONG),
        ("MulticastMgmtAlgorithmsList", DOT11_AUTH_CIPHER_PAIR),
        ("NumSecondaryStaBandCombinations", ULONG),
        ("SecondaryStaBandsCombinations", WIFI_STA_BANDS_COMBINATION),
        ("MaxMLOLinksSupported", ULONG),
        ("DoNotUseOsReserved", BOOLEAN),
        ("MLOAddressesList", WDI_MAC_ADDRESS),
        ("NumAkmsSupported", ULONG),
        ("AkmsList", RSNA_AKM_SUITE),
        ("NumFIPSCertifiedCipherAlgorithms", ULONG),
        ("FIPSCertifiedCipherAlgorithmsList", WDI_CIPHER_ALGORITHM_T),
        ("MSCSSupported", BOOLEAN),
        ("DSCPToUPMappingSupported", BOOLEAN),
        ("MaxNumConfigurableActionFrameWakePatterns", UINT32),
        ("CrossAkmCipherRoamSupported", BOOLEAN)
    ]


class Win32_Wlan:

    def __init__(self):
        self._handle = self.WlanOpenHandle()
        self._wlanapi = ct.windll.LoadLibrary("wlanapi.dll")

    def WlanOpenHandle(self):
        """
        DWORD WlanOpenHandle(
        [In] DWORD dwClientVersion,
        [Reserved] PVOID pReserved,
        [Out] PWORD pdwNegotiatedVersion
        [Out] PHANDLE phClientHandle
        )
        """
        func_ref = self._wlanapi.WlanOpenHandle
        func_ref.argtypes = [DWORD, ct.c_void_p, ct.POINTER(DWORD), ct.POINTER(HANDLE)]  #func argument types 
        func_ref.restype = DWORD  #func return type
        negotiated_ver = DWORD()  #dword holder for pdwNegotiatedVersion reference
        client_handle = HANDLE()  #handle holder for client handle reference
        client_ver = 2  #predefined value client version for newer windows versions
        p_reserved = None  #void variable for reserved param
        res = func_ref(client_ver, p_reserved, ct.byref(negotiated_ver), ct.byref(client_handle))  #byref() used for [Out] params that will be assigned value
        if res != ERROR_SUCCESS:
            raise Exception("Error trying to open wlan handle")
        return client_handle

    def WlanCloseHandle(self):
        """
        DWORD WlanCloseHandle(
        [In] HANDLE pClientHandle,
        [Reserved] PVOID pReserved
        )
        """
        func_ref = self._wlanapi.WlanCloseHandle
        func_ref.argtypes = [HANDLE, ct.c_void_p]
        func_ref.restype = DWORD
        res = func_ref(self._handle, None)
        if res != ERROR_SUCCESS:
            raise Exception("Error closing wlan handle")
        return res

    def WifiDeviceSetStationCapabilities(self):
        pass

