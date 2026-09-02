"""Application configuration for CyberQuant AI.

All tunable coefficients used by the risk engine and enterprise-score
normalization live here so they have documented provenance (per the
risk-engine specification, section 14: "Source-of-Truth Implementation Rules").
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CYBERQUANT_", env_file=".env")

    # --- General ---
    app_name: str = "CyberQuant AI"
    api_prefix: str = "/api"
    currency: str = "INR"
    data_status: str = "SIMULATED"  # SIMULATED | LIVE

    # --- Database ---
    database_url: str = "sqlite:///./cyberquant.db"

    # --- Risk engine coefficients (docs/04-risk-engine.md) ---
    base_probability_floor: float = 0.05
    base_probability_cvss_weight: float = 0.35
    multiplier_criticality: float = 0.20
    multiplier_exposure: float = 0.20
    multiplier_exploitability: float = 0.15
    multiplier_threat: float = 0.15
    multiplier_data_sensitivity: float = 0.10

    # --- Enterprise risk score normalization (section 8) ---
    # Reference annual exposure used to normalize the 0-100 score.
    # Documented configuration value, never hidden in code.
    reference_exposure: float = 500_000_000.0  # ₹50 crore reference

    # --- CORS ---
    frontend_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.frontend_origins.split(",") if o.strip()]


settings = Settings()
