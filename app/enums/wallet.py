from enum import Enum

class WalletState(str, Enum):

    LIVE = "LIVE"

    FROZEN = "FRONZE"

    ARCHIVED = "ARCHIVED"

class Blockchain(str, Enum):

    ETH_SEPOLIA = "ETH-SEPOLIA"

    ARB_SEPOLIA = "ARB-SEPOLIA"

    BASE_SEPOLIA = "BASE-SEPOLIA"

    POLYGON_AMOY = "POLYGON-AMOY"