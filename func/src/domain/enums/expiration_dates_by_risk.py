from regis import RiskRatings
from enum import Enum


class RiskRatingExpirationDates(RiskRatings):
    LOW_RISK = 5
    MODERATE_RISK = 3
    HIGH_RISK = 1
    CRITICAL_RISK = 0.5
