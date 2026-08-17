"""
Tamil Nadu GIS Coordinates & Spatial Analytics Engine
Contains exact latitude/longitude coordinates for all 38 Tamil Nadu districts,
color scale mappers, and interactive popup HTML generators.
"""

from typing import Dict, Tuple, Any

# Accurate GPS Centroid Coordinates for all 38 Tamil Nadu Districts
TN_DISTRICT_COORDINATES: Dict[str, Tuple[float, float]] = {
    "Ariyalur": (11.1401, 79.0786),
    "Chengalpattu": (12.6841, 79.9836),
    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Cuddalore": (11.7480, 79.7714),
    "Dharmapuri": (12.1211, 78.1582),
    "Dindigul": (10.3673, 77.9803),
    "Erode": (11.3410, 77.7172),
    "Kallakurichi": (11.7384, 78.9639),
    "Kanchipuram": (12.8342, 79.7036),
    "Kanyakumari": (8.0883, 77.5385),
    "Karur": (10.9601, 78.0766),
    "Krishnagiri": (12.5186, 78.2137),
    "Madurai": (9.9252, 78.1198),
    "Mayiladuthurai": (11.1018, 79.6522),
    "Nagapattinam": (10.7672, 79.8449),
    "Namakkal": (11.2189, 78.1674),
    "Nilgiris": (11.4916, 76.7337),
    "Perambalur": (11.2342, 78.8820),
    "Pudukkottai": (10.3797, 78.8208),
    "Ramanathapuram": (9.3639, 78.8395),
    "Ranipet": (12.9271, 79.3333),
    "Salem": (11.6643, 78.1460),
    "Sivaganga": (9.8433, 78.4809),
    "Tenkasi": (8.9593, 77.3146),
    "Thanjavur": (10.7870, 79.1378),
    "Theni": (10.0104, 77.4768),
    "Thoothukudi": (8.7642, 78.1348),
    "Tiruchirappalli": (10.7905, 78.7047),
    "Tirunelveli": (8.7139, 77.7567),
    "Tirupathur": (12.4929, 78.5678),
    "Tiruppur": (11.1085, 77.3411),
    "Tiruvallur": (13.1432, 79.9079),
    "Tiruvannamalai": (12.2253, 79.0747),
    "Tiruvarur": (10.7725, 79.6365),
    "Vellore": (12.9165, 79.1325),
    "Viluppuram": (11.9401, 79.4861),
    "Virudhunagar": (9.5680, 77.9624)
}

def get_district_coordinates(district_name: str) -> Tuple[float, float]:
    """
    Returns (latitude, longitude) centroid for a given district.
    Defaults to TN central coordinates if missing.
    """
    return TN_DISTRICT_COORDINATES.get(district_name.strip(), (11.1271, 78.6569))

def get_color_for_metric(val: float, metric_type: str = "deficit") -> str:
    """
    Returns hex color based on metric threshold value.
    - Deficit Score: Red for high deficit (>75), Amber (50-75), Green (<50).
    - Congestion: Red for high congestion (>20), Amber (10-20), Green (<10).
    """
    if metric_type == "deficit":
        if val >= 75.0:
            return "#EF4444"  # Red
        elif val >= 50.0:
            return "#F59E0B"  # Amber / Yellow
        else:
            return "#10B981"  # Emerald Green
    elif metric_type == "congestion":
        if val >= 20.0:
            return "#DC2626"  # Deep Red
        elif val >= 10.0:
            return "#F59E0B"  # Amber
        else:
            return "#3B82F6"  # Blue
    elif metric_type == "freight":
        if val >= 40.0:
            return "#8B5CF6"  # Purple
        elif val >= 20.0:
            return "#3B82F6"  # Blue
        else:
            return "#06B6D4"  # Cyan
    return "#3B82F6"

def build_district_popup_html(row: Dict[str, Any]) -> str:
    """
    Generates a dark-themed HTML popup card for Folium map markers.
    """
    name = row.get("district_name", "N/A")
    region = row.get("region", "N/A")
    freight = row.get("freight_volume_million_tonnes", 0.0)
    gddp = row.get("gddp_cr", 0.0)
    density = row.get("road_density", 0.0)
    congestion = row.get("congestion_index", 0.0)
    deficit = row.get("infrastructure_deficit_score", 0.0)
    warehouses = row.get("warehouses", 0)
    parks = row.get("logistics_parks", 0)
    budget = row.get("recommended_budget_cr", 0.0)

    deficit_color = "#EF4444" if deficit >= 75 else "#F59E0B" if deficit >= 50 else "#10B981"

    html = f"""
    <div style="font-family: Arial, sans-serif; background-color: #0F172A; color: #F8FAFC; padding: 14px; border-radius: 8px; width: 250px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); border: 1px solid #334155;">
        <div style="font-size: 16px; font-weight: bold; color: #60A5FA; border-bottom: 1px solid #334155; padding-bottom: 6px; margin-bottom: 8px;">
            📍 {name} <span style="font-size: 11px; color: #94A3B8; font-weight: normal;">({region})</span>
        </div>
        <div style="font-size: 12px; line-height: 1.6;">
            🚚 <strong>Annual Freight:</strong> {freight:.2f} M Tonnes<br/>
            💰 <strong>GDDP:</strong> ₹ {gddp:,.0f} Cr<br/>
            🛣️ <strong>Road Density:</strong> {density:.2f} km/100 km²<br/>
            🚥 <strong>Congestion Index:</strong> {congestion:.1f}<br/>
            🏭 <strong>Warehouses:</strong> {warehouses} | <strong>Parks:</strong> {parks}<br/>
            <hr style="border: 0; border-top: 1px solid #334155; margin: 6px 0;"/>
            ⚠️ <strong>Deficit Score:</strong> <span style="color: {deficit_color}; font-weight: bold;">{deficit:.1f} / 100</span><br/>
            💵 <strong>Rec. Budget:</strong> <span style="color: #34D399; font-weight: bold;">₹ {budget:,.0f} Cr</span>
        </div>
    </div>
    """
    return html
